# Vue 3 + Pinia + Vite + TypeScript 实现 ECharts 仪表板

下面是将你的 ECharts 仪表板转换为 Vue 3 项目的完整实现，按照组件化方式拆分。

## 项目结构

```
src/
├── assets/
├── components/
│   ├── charts/
│   │   ├── DlRsrpChart.vue
│   │   ├── DlThroughputChart.vue
│   │   └── UlThroughputChart.vue
│   └── DashboardContainer.vue
├── stores/
│   └── chartData.ts
├── App.vue
├── main.ts
├── vite-env.d.ts
```

## 1. 安装依赖

首先安装必要的依赖：

```bash
npm install echarts pinia vue-echarts
npm install -D @types/echarts
```

## 2. 创建 Pinia Store (数据存储)

`src/stores/chartData.ts`

```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useChartDataStore = defineStore('chartData', () => {
  // 生成时间轴数据
  const generateTimeData = (count: number): string[] => {
    return Array.from({ length: count }, (_, i) => {
      const date = new Date();
      date.setMinutes(date.getMinutes() - count + i);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
  };

  // 生成随机数据
  const generateRandomData = (count: number, min: number, max: number): number[] => {
    return Array.from({ length: count }, () => 
      Math.floor(Math.random() * (max - min + 1)) + min
    );
  };

  // UL Throughput 数据
  const ulData = ref(generateRandomData(20, 10, 100));
  const ulTimeData = ref(generateTimeData(20));
  
  // DL Throughput 数据
  const dlData = ref(generateRandomData(20, 50, 250));
  const dlTimeData = ref(generateTimeData(20));
  
  // DL RSRP 数据
  const rsrpData = ref(generateRandomData(20, -110, -80));
  const rsrpTimeData = ref(generateTimeData(20));

  // 更新数据
  const updateData = () => {
    ulData.value = [...ulData.value.slice(1), generateRandomData(1, 10, 100)[0]];
    dlData.value = [...dlData.value.slice(1), generateRandomData(1, 50, 250)[0]];
    rsrpData.value = [...rsrpData.value.slice(1), generateRandomData(1, -110, -80)[0]];
    
    ulTimeData.value = generateTimeData(20);
    dlTimeData.value = generateTimeData(20);
    rsrpTimeData.value = generateTimeData(20);
  };

  // 开始定时更新
  const startDataUpdates = () => {
    setInterval(updateData, 2000);
  };

  return {
    ulData,
    ulTimeData,
    dlData,
    dlTimeData,
    rsrpData,
    rsrpTimeData,
    startDataUpdates
  };
});
```

## 3. 创建图表组件

### UL Throughput 图表组件

`src/components/charts/UlThroughputChart.vue`

```vue
<template>
  <div ref="chartRef" style="width: 100%; height: 100%"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import { useChartDataStore } from '@/stores/chartData';

const chartRef = ref<HTMLElement>();
let chart: echarts.ECharts | null = null;

const chartDataStore = useChartDataStore();

const colors = {
  line: '#00ff88',
  areaStart: '#00ff88dd',
  areaEnd: '#00b4d900'
};

const initChart = () => {
  if (!chartRef.value) return;
  
  chart = echarts.init(chartRef.value);
  
  const option = {
    grid: { top: 15, left: 50, right: 30, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        return `${params[0].axisValue}<br/>
        <span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${colors.line};"></span>
        UL Throughput: ${params[0].value} Mbps`;
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartDataStore.ulTimeData,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { color: '#8a9bb8' }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 120,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { 
        color: '#8a9bb8',
        formatter: (value: number) => value + ' Mbps'
      },
      splitLine: { lineStyle: { color: '#1a2a40' }}
    },
    series: [{
      name: 'UL Throughput',
      type: 'line',
      showSymbol: false,
      data: chartDataStore.ulData,
      smooth: true,
      lineStyle: {
        width: 2,
        color: colors.line
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: colors.areaStart },
          { offset: 1, color: colors.areaEnd }
        ])
      },
      emphasis: {
        lineStyle: {
          width: 3,
          shadowColor: colors.line,
          shadowBlur: 10
        }
      }
    }],
    animationDuration: 1500
  };

  chart.setOption(option);
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', () => chart?.resize());
});

watch(
  () => [chartDataStore.ulData, chartDataStore.ulTimeData],
  () => {
    if (chart) {
      chart.setOption({
        xAxis: {
          data: chartDataStore.ulTimeData
        },
        series: [{
          data: chartDataStore.ulData
        }]
      });
    }
  },
  { deep: true }
);
</script>
```

### DL Throughput 图表组件

`src/components/charts/DlThroughputChart.vue`

```vue
<template>
  <div ref="chartRef" style="width: 100%; height: 100%"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import { useChartDataStore } from '@/stores/chartData';

const chartRef = ref<HTMLElement>();
let chart: echarts.ECharts | null = null;

const chartDataStore = useChartDataStore();

const colors = {
  line: '#ff7675',
  areaStart: '#ff7675dd',
  areaEnd: '#d6303100'
};

const initChart = () => {
  if (!chartRef.value) return;
  
  chart = echarts.init(chartRef.value);
  
  const option = {
    grid: { top: 15, left: 50, right: 30, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        return `${params[0].axisValue}<br/>
        <span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${colors.line};"></span>
        DL Throughput: ${params[0].value} Mbps`;
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartDataStore.dlTimeData,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { color: '#8a9bb8' }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 300,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { 
        color: '#8a9bb8',
        formatter: (value: number) => value + ' Mbps'
      },
      splitLine: { lineStyle: { color: '#1a2a40' }}
    },
    series: [{
      name: 'DL Throughput',
      type: 'line',
      showSymbol: false,
      data: chartDataStore.dlData,
      smooth: true,
      lineStyle: {
        width: 2,
        color: colors.line
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: colors.areaStart },
          { offset: 1, color: colors.areaEnd }
        ])
      },
      emphasis: {
        lineStyle: {
          width: 3,
          shadowColor: colors.line,
          shadowBlur: 10
        }
      }
    }],
    animationDuration: 1500
  };

  chart.setOption(option);
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', () => chart?.resize());
});

watch(
  () => [chartDataStore.dlData, chartDataStore.dlTimeData],
  () => {
    if (chart) {
      chart.setOption({
        xAxis: {
          data: chartDataStore.dlTimeData
        },
        series: [{
          data: chartDataStore.dlData
        }]
      });
    }
  },
  { deep: true }
);
</script>
```

### DL RSRP 图表组件

`src/components/charts/DlRsrpChart.vue`

```vue
<template>
  <div ref="chartRef" style="width: 100%; height: 100%"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import { useChartDataStore } from '@/stores/chartData';

const chartRef = ref<HTMLElement>();
let chart: echarts.ECharts | null = null;

const chartDataStore = useChartDataStore();

const colors = {
  line: '#6c5ce7',
  areaStart: '#6c5ce7dd',
  areaEnd: '#0984e300'
};

const initChart = () => {
  if (!chartRef.value) return;
  
  chart = echarts.init(chartRef.value);
  
  const option = {
    grid: { top: 15, left: 50, right: 30, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        return `${params[0].axisValue}<br/>
        <span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${colors.line};"></span>
        DL RSRP: ${params[0].value} dBm`;
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartDataStore.rsrpTimeData,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { color: '#8a9bb8' }
    },
    yAxis: {
      type: 'value',
      min: -120,
      max: -70,
      axisLine: { lineStyle: { color: '#4a5e7a' }},
      axisLabel: { 
        color: '#8a9bb8',
        formatter: (value: number) => value + ' dBm'
      },
      splitLine: { lineStyle: { color: '#1a2a40' }}
    },
    series: [{
      name: 'DL RSRP',
      type: 'line',
      showSymbol: false,
      data: chartDataStore.rsrpData,
      smooth: true,
      lineStyle: {
        width: 2,
        color: colors.line
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: colors.areaStart },
          { offset: 1, color: colors.areaEnd }
        ])
      },
      emphasis: {
        lineStyle: {
          width: 3,
          shadowColor: colors.line,
          shadowBlur: 10
        }
      }
    }],
    animationDuration: 1500
  };

  chart.setOption(option);
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', () => chart?.resize());
});

watch(
  () => [chartDataStore.rsrpData, chartDataStore.rsrpTimeData],
  () => {
    if (chart) {
      chart.setOption({
        xAxis: {
          data: chartDataStore.rsrpTimeData
        },
        series: [{
          data: chartDataStore.rsrpData
        }]
      });
    }
  },
  { deep: true }
);
</script>
```

## 4. 创建 Dashboard 容器组件

`src/components/DashboardContainer.vue`

```vue
<template>
  <div class="dashboard">
    <!-- UL Throughput -->
    <div class="chart-container">
      <div class="chart-title">UL Throughput (Mbps)</div>
      <UlThroughputChart />
    </div>

    <!-- DL Throughput -->
    <div class="chart-container">
      <div class="chart-title">DL Throughput (Mbps)</div>
      <DlThroughputChart />
    </div>

    <!-- DL RSRP -->
    <div class="chart-container">
      <div class="chart-title">DL RSRP (dBm)</div>
      <DlRsrpChart />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useChartDataStore } from '@/stores/chartData';
import UlThroughputChart from './charts/UlThroughputChart.vue';
import DlThroughputChart from './charts/DlThroughputChart.vue';
import DlRsrpChart from './charts/DlRsrpChart.vue';

const chartDataStore = useChartDataStore();

onMounted(() => {
  chartDataStore.startDataUpdates();
});
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-container {
  background: rgba(12, 25, 50, 0.8);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.2);
  padding: 10px;
  height: 350px;
}

.chart-title {
  color: #00f7ff;
  font-size: 18px;
  padding: 10px 15px;
  border-left: 4px solid #00f7ff;
  text-shadow: 0 0 10px rgba(0, 247, 255, 0.5);
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
}
</style>
```

## 5. 主应用文件

`src/App.vue`

```vue
<template>
  <div class="app">
    <DashboardContainer />
  </div>
</template>

<script setup lang="ts">
import DashboardContainer from './components/DashboardContainer.vue';
</script>

<style>
body {
  background-color: #0a1930;
  margin: 0;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.app {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
```

## 6. 主入口文件

`src/main.ts`

```typescript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

const app = createApp(App);

app.use(createPinia());

app.mount('#app');
```

## 7. 类型声明文件

`src/vite-env.d.ts`

```typescript
/// <reference types="vite/client" />
```

## 项目配置

确保你的 `vite.config.ts` 文件配置了 Vue 和 TypeScript 支持：

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});
```

## 说明

1. **项目结构**：
   - 使用 Pinia 作为状态管理，集中管理所有图表数据
   - 每个图表拆分为独立组件，便于维护和复用
   - Dashboard 容器组件负责布局和启动数据更新

2. **数据流**：
   - Pinia store 生成和管理所有数据
   - 组件通过 store 获取数据并渲染图表
   - 数据更新通过 watch 响应式触发图表更新

3. **响应式设计**：
   - 图表自动响应窗口大小变化
   - 布局适应不同屏幕尺寸
   - 保留了原始项目的所有视觉效果

4. **TypeScript 支持**：
   - 所有组件和 store 都有类型定义
   - 使用 Composition API 和 `<script setup>` 语法

这个实现保持了原始 HTML 版本的所有功能，同时利用了 Vue 3 的响应式特性和组件化架构，使代码更易于维护和扩展。
