<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from "vue";
import * as echarts from "echarts";
import { useBsStore } from "@/stores/index";
import { storeToRefs } from "pinia";

type ChartOption = echarts.EChartsOption;

const chartDom = ref<HTMLElement>();
let myChart: echarts.ECharts | null = null;
const timer = ref<number>();

const props = defineProps({
  autoResize: {
    type: Boolean,
    default: true,
  },
});

let resizeObserver: ResizeObserver;

// 使用socket store
const socketStore = useBsStore();
const { bsData } = storeToRefs(socketStore);

// 初始化数据
const startTimestamp = ref(Date.now()); // 记录起始时间戳
const duration = 60; // 显示60秒数据
const timeOffset = ref(0); // 当前时间偏移（秒）
const downlinkData = ref<Array<[number, number]>>([]); // [时间偏移, 值]
const uplinkData = ref<Array<[number, number]>>([]); // [时间偏移, 值]

// 初始化60秒空数据
for (let i = duration - 1; i >= 0; i--) {
  const offset = -i;
  downlinkData.value.push([offset, 0]);
  uplinkData.value.push([offset, 0]);
}

// 参考线配置
const markLineCfg = {
  symbol: "none",
  data: [
    {
      yAxis: 10000,
      label: {
        show: true,
        formatter: "",
        color: "#fff",
      },
      lineStyle: {
        type: "solid" as "solid",
        color: "rgba(233, 240, 48)",
        width: 1,
      },
    },
  ],
};

// 图表配置
const option: ChartOption = {
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
      shadowStyle: {
        color: "rgba(0, 150, 255, 0.3)",
      },
    },
    formatter: (params: any) => {
      const offset = params[0].value[0];
      const actualTime = new Date(startTimestamp.value + offset * 1000);
      const h = actualTime.getHours().toString().padStart(2, '0');
      const m = actualTime.getMinutes().toString().padStart(2, '0');
      const s = actualTime.getSeconds().toString().padStart(2, '0');
      const timeStr = `${h}:${m}:${s}`;
      
      let result = timeStr + "<br/>";
      params.forEach((item: any) => {
        result += `${item.marker} ${
          item.seriesName
        }: <strong>${item.value[1].toFixed(2)} Mbps</strong><br/>`;
      });
      return result;
    },
  },
  legend: {
    data: ["下行流量", "上行流量"],
    textStyle: {
      color: "#fff",
    },
    right: 10,
    top: 10,
    itemStyle: {
      borderWidth: 0,
    },
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  xAxis: {
    type: "value",
    min: -duration,
    max: 0,
    interval: 10,
    axisLine: {
      lineStyle: {
        color: "rgba(0, 198, 255, 0.5)",
      },
    },
    axisLabel: {
      color: "rgba(255, 255, 255, 0.8)",
      fontSize: 12,
      formatter: (value: number) => {
        const time = new Date(startTimestamp.value + value * 1000);
        const h = time.getHours().toString().padStart(2, '0');
        const m = time.getMinutes().toString().padStart(2, '0');
        const s = time.getSeconds().toString().padStart(2, '0');
        return `${h}:${m}:${s}`;
      }
    },
    axisTick: {
      alignWithLabel: true,
      lineStyle: {
        color: "rgba(0, 198, 255, 0.3)",
      },
    },
  },
  yAxis: {
    type: "value",
    name: "流量 (Mbps)",
    max: 12000,
    min: 0,
    nameTextStyle: {
      color: "rgba(255, 255, 255, 0.8)",
      padding: [0, 0, 0, 40],
    },
    splitLine: {
      lineStyle: {
        color: "rgba(0, 198, 255, 0.1)",
      },
    },
    axisLine: {
      lineStyle: {
        color: "rgba(0, 198, 255, 0.5)",
      },
    },
    axisLabel: {
      color: "rgba(255, 255, 255, 0.8)",
    },
  },
  series: [
    {
      name: "下行流量",
      type: "line",
      lineStyle: {
        width: 1,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          {
            offset: 0,
            color: "#00c6ff",
          },
          {
            offset: 1,
            color: "#0072ff",
          },
        ]),
      },
      showSymbol: false,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: "rgba(0, 198, 255, 0.5)",
          },
          {
            offset: 1,
            color: "rgba(0, 114, 255, 0.1)",
          },
        ]),
      },
      emphasis: {
        focus: "series",
      },
      data: downlinkData.value,
      markLine: markLineCfg,
    },
    {
      name: "上行流量",
      type: "line",
      smooth: false,
      lineStyle: {
        width: 1,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          {
            offset: 0,
            color: "#ff6a00",
          },
          {
            offset: 1,
            color: "#ee0979",
          },
        ]),
      },
      showSymbol: false,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: "rgba(255, 106, 0, 0.5)",
          },
          {
            offset: 1,
            color: "rgba(238, 9, 121, 0.1)",
          },
        ]),
      },
      emphasis: {
        focus: "series",
      },
      data: uplinkData.value,
      markLine: markLineCfg,
    },
  ],
  animationEasing: "elasticOut",
  animationDelayUpdate: (idx: number) => idx * 5,
};

// 监听bsData变化
watch(
  bsData,
  (newData) => {
    if (!newData) return;

    // 更新时间偏移
    timeOffset.value = (Date.now() - startTimestamp.value) / 1000;
    
    // 添加新数据点
    const downlinkValue = Number(newData.DLRlcTotal) / 1000000 || 0;
    const uplinkValue = Number(newData.ULRlcToal) / 1000000 || 0;
    
    downlinkData.value.push([timeOffset.value, downlinkValue]);
    uplinkData.value.push([timeOffset.value, uplinkValue]);
    
    // 移除旧数据点（保持60秒窗口）
    if (downlinkData.value.length > duration) {
      downlinkData.value.shift();
      uplinkData.value.shift();
    }
    
    // 更新图表
    if (myChart) {
      // 计算x轴范围（显示最近60秒）
      const xMin = Math.max(timeOffset.value - duration, -duration);
      const xMax = timeOffset.value;
      
      myChart.setOption({
        xAxis: {
          min: xMin,
          max: xMax
        },
        series: [
          { data: downlinkData.value },
          { data: uplinkData.value }
        ]
      });
    }
  },
  { deep: true }
);

onMounted(() => {
  if (chartDom.value) {
    myChart = echarts.init(chartDom.value);
    myChart.setOption(option);

    // 窗口resize处理
    const handleResize = () => myChart?.resize();
    window.addEventListener("resize", handleResize);

    // 组件卸载时清理
    onUnmounted(() => {
      if (timer.value) clearInterval(timer.value);
      window.removeEventListener("resize", handleResize);
      myChart?.dispose();
    });
  }
  
  if (props.autoResize && chartDom.value) {
    resizeObserver = new ResizeObserver(() => {
      myChart?.resize();
    });
    resizeObserver.observe(chartDom.value);
  }
});

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>
