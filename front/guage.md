# Vue 3 + TypeScript 科技感网络速率仪表盘组件

下面是将上述ECharts仪表盘转换为Vue 3 + TypeScript组件的实现：

## 组件代码

```typescript
<template>
  <div class="network-speed-dashboard">
    <div class="title">网络速率监控仪表盘</div>
    <div ref="gaugeChart" class="gauge-chart"></div>
    <div class="stats">
      <div class="stat-box">
        <div class="stat-label">下载速度</div>
        <div class="stat-value">{{ downloadSpeed }} Mbps</div>
        <div class="stat-label">峰值: {{ downloadMax }} Mbps</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">上传速度</div>
        <div class="stat-value">{{ uploadSpeed }} Mbps</div>
        <div class="stat-label">峰值: {{ uploadMax }} Mbps</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount, ref } from 'vue';
import * as echarts from 'echarts';

export default defineComponent({
  name: 'NetworkSpeedDashboard',
  props: {
    downloadMax: {
      type: Number,
      default: 120
    },
    uploadMax: {
      type: Number,
      default: 60
    },
    updateInterval: {
      type: Number,
      default: 2000
    },
    useRealData: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const gaugeChart = ref<HTMLElement | null>(null);
    let chartInstance: echarts.ECharts | null = null;
    const downloadSpeed = ref(0);
    const uploadSpeed = ref(0);
    let updateTimer: number | null = null;

    // 初始化图表
    const initChart = () => {
      if (!gaugeChart.value) return;

      chartInstance = echarts.init(gaugeChart.value);
      const option = getChartOption();
      chartInstance.setOption(option);
      
      // 响应式调整
      window.addEventListener('resize', handleResize);
    };

    // 获取图表配置
    const getChartOption = (): echarts.EChartsOption => {
      return {
        backgroundColor: 'transparent',
        tooltip: {
          formatter: '{a} <br/>{b} : {c}Mbps'
        },
        series: [
          {
            name: '下载速度',
            type: 'gauge',
            min: 0,
            max: props.downloadMax,
            splitNumber: 6,
            radius: '90%',
            axisLine: {
              lineStyle: {
                width: 30,
                color: [
                  [0.3, '#67e0e3'],
                  [0.7, '#37a2da'],
                  [1, '#fd666d']
                ]
              }
            },
            pointer: {
              itemStyle: {
                color: 'auto'
              }
            },
            axisTick: {
              distance: -30,
              length: 8,
              lineStyle: {
                color: '#fff',
                width: 2
              }
            },
            splitLine: {
              distance: -30,
              length: 30,
              lineStyle: {
                color: '#fff',
                width: 4
              }
            },
            axisLabel: {
              color: 'auto',
              distance: 40,
              fontSize: 14
            },
            detail: {
              valueAnimation: true,
              formatter: '{value} Mbps',
              color: 'auto',
              fontSize: 20,
              offsetCenter: [0, '70%']
            },
            data: [
              {
                value: downloadSpeed.value,
                name: '下载速度'
              }
            ],
            title: {
              offsetCenter: [0, '-30%'],
              fontSize: 16,
              color: '#7fdbff'
            }
          },
          {
            name: '上传速度',
            type: 'gauge',
            min: 0,
            max: props.uploadMax,
            splitNumber: 6,
            radius: '65%',
            axisLine: {
              lineStyle: {
                width: 20,
                color: [
                  [0.3, '#9FE6B8'],
                  [0.7, '#32C5E9'],
                  [1, '#FFDB5C']
                ]
              }
            },
            pointer: {
              itemStyle: {
                color: 'auto'
              }
            },
            axisTick: {
              distance: -20,
              length: 6,
              lineStyle: {
                color: '#fff',
                width: 2
              }
            },
            splitLine: {
              distance: -20,
              length: 20,
              lineStyle: {
                color: '#fff',
                width: 3
              }
            },
            axisLabel: {
              color: 'auto',
              distance: 30,
              fontSize: 12
            },
            detail: {
              valueAnimation: true,
              formatter: '{value} Mbps',
              color: 'auto',
              fontSize: 16,
              offsetCenter: [0, '50%']
            },
            data: [
              {
                value: uploadSpeed.value,
                name: '上传速度'
              }
            ],
            title: {
              offsetCenter: [0, '-20%'],
              fontSize: 14,
              color: '#7fdbff'
            }
          }
        ]
      };
    };

    // 更新数据
    const updateData = () => {
      if (props.useRealData) {
        // 这里可以替换为真实的网络速度获取逻辑
        // 例如调用API或使用WebRTC等
        fetchNetworkSpeed();
      } else {
        // 模拟数据
        downloadSpeed.value = getRandomSpeed(props.downloadMax);
        uploadSpeed.value = getRandomSpeed(props.uploadMax);
      }

      if (chartInstance) {
        const option = getChartOption();
        chartInstance.setOption(option);
      }

      // 设置下次更新
      updateTimer = window.setTimeout(updateData, props.updateInterval);
    };

    // 模拟获取网络速度
    const getRandomSpeed = (max: number): number => {
      return Math.floor(Math.random() * max * 0.9 + max * 0.1);
    };

    // 获取真实网络速度（示例）
    const fetchNetworkSpeed = () => {
      // 这里应该是实际的网络速度获取逻辑
      // 由于浏览器限制，获取真实网络速度可能需要使用特定API或扩展
      console.log('Fetching real network speed...');
      downloadSpeed.value = getRandomSpeed(props.downloadMax);
      uploadSpeed.value = getRandomSpeed(props.uploadMax);
    };

    // 处理窗口大小变化
    const handleResize = () => {
      if (chartInstance) {
        chartInstance.resize();
      }
    };

    // 组件挂载时初始化
    onMounted(() => {
      initChart();
      updateData();
    });

    // 组件卸载前清理
    onBeforeUnmount(() => {
      if (updateTimer) {
        clearTimeout(updateTimer);
      }
      if (chartInstance) {
        chartInstance.dispose();
        window.removeEventListener('resize', handleResize);
      }
    });

    return {
      gaugeChart,
      downloadSpeed,
      uploadSpeed
    };
  }
});
</script>

<style scoped>
.network-speed-dashboard {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #0a1a2e;
  color: #fff;
  font-family: 'Arial', sans-serif;
  padding: 20px;
  box-sizing: border-box;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
  color: #00f2ff;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

.gauge-chart {
  width: 600px;
  height: 500px;
}

.stats {
  display: flex;
  justify-content: space-around;
  width: 600px;
  margin-top: 20px;
}

.stat-box {
  background: rgba(10, 30, 50, 0.7);
  border: 1px solid #00f2ff;
  border-radius: 5px;
  padding: 15px;
  width: 45%;
  text-align: center;
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
}

.stat-value {
  font-size: 24px;
  color: #00f2ff;
  margin: 10px 0;
}

.stat-label {
  font-size: 16px;
  color: #7fdbff;
}

@media (max-width: 768px) {
  .gauge-chart {
    width: 100%;
    height: 400px;
  }
  
  .stats {
    width: 100%;
    flex-direction: column;
    align-items: center;
  }
  
  .stat-box {
    width: 80%;
    margin-bottom: 15px;
  }
}
</style>
```

## 组件使用示例

```typescript
<template>
  <div>
    <NetworkSpeedDashboard 
      :download-max="150" 
      :upload-max="75" 
      :update-interval="3000"
      :use-real-data="false"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import NetworkSpeedDashboard from './components/NetworkSpeedDashboard.vue';

export default defineComponent({
  name: 'App',
  components: {
    NetworkSpeedDashboard
  }
});
</script>
```

## 组件特点

1. **TypeScript支持**：
   - 完整的类型定义
   - 明确的props类型检查

2. **可配置属性**：
   - `downloadMax`: 下载速度最大值 (默认120Mbps)
   - `uploadMax`: 上传速度最大值 (默认60Mbps)
   - `updateInterval`: 数据更新间隔 (默认2000ms)
   - `useRealData`: 是否使用真实数据 (默认false，使用模拟数据)

3. **响应式设计**：
   - 自动适应容器大小变化
   - 移动端适配

4. **生命周期管理**：
   - 组件卸载时自动清理定时器和图表实例

5. **扩展性**：
   - 提供了`fetchNetworkSpeed`方法占位，方便接入真实数据源

## 真实数据接入建议

要获取真实的网络速度数据，你可以：

1. 使用WebRTC的统计API
2. 实现一个简单的测速逻辑（下载/上传测试文件并计算速度）
3. 接入第三方测速服务API

只需在`fetchNetworkSpeed`方法中实现你的真实数据获取逻辑即可。
