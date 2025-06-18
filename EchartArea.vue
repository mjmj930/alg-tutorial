<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

// 显示秒数长度
const duration = 60;
let currentTime = 0;
const chartRef = ref<HTMLDivElement | null>(null);

let chart: echarts.ECharts;
let timer: number;
const uplinkData: [number, number][] = [];
const downlinkData: [number, number][] = [];

// 起始时间戳
const startTimestamp = Date.now();

onMounted(() => {
  if (!chartRef.value) return;

  chart = echarts.init(chartRef.value);

  const option: echarts.EChartsOption = {
    title: {
      text: '上行 / 下行 动态折线面积图'
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const offsetSec = params[0].value[0];
        const actualTime = new Date(startTimestamp + offsetSec * 1000);
        const timeStr = actualTime.toLocaleTimeString();
        return `${timeStr}<br/>` + params.map((p: any) => `${p.seriesName}: ${p.value[1]}`).join('<br/>');
      }
    },
    legend: {
      data: ['上行', '下行']
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: duration,
      interval: 10,
      axisLabel: {
        formatter: (value: number) => {
          const time = new Date(startTimestamp + value * 1000);
          const h = time.getHours().toString().padStart(2, '0');
          const m = time.getMinutes().toString().padStart(2, '0');
          const s = time.getSeconds().toString().padStart(2, '0');
          return `${h}:${m}:${s}`;
        }
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '上行',
        type: 'line',
        areaStyle: { color: 'rgba(0, 150, 255, 0.3)' },
        lineStyle: { color: 'rgba(0, 150, 255, 1)' },
        showSymbol: false,
        data: []
      },
      {
        name: '下行',
        type: 'line',
        areaStyle: { color: 'rgba(255, 100, 100, 0.3)' },
        lineStyle: { color: 'rgba(255, 100, 100, 1)' },
        showSymbol: false,
        data: []
      }
    ],
    animation: false
  };

  chart.setOption(option);

  // 模拟动态添加数据
  timer = window.setInterval(() => {
    const uplink = Math.floor(Math.random() * 60 + 20);
    const downlink = Math.floor(Math.random() * 60 + 10);

    uplinkData.push([currentTime, uplink]);
    downlinkData.push([currentTime, downlink]);

    let xMin = 0;
    let xMax = duration;
    if (currentTime > duration) {
      xMin = currentTime - duration;
      xMax = currentTime;
    }

    chart.setOption({
      xAxis: {
        min: xMin,
        max: xMax
      },
      series: [
        { name: '上行', data: uplinkData },
        { name: '下行', data: downlinkData }
      ]
    });

    currentTime += 1;
  }, 1000);
});

onBeforeUnmount(() => {
  clearInterval(timer);
  chart?.dispose();
});
</script>
