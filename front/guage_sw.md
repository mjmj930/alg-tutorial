# Vue 3 网络速度仪表盘组件

下面是将您的HTML代码转换为Vue 3组件的实现：

## 组件代码 (NetworkSpeedGauge.vue)

```vue
<template>
  <div class="dashboard">
    <!-- 速度仪表盘 -->
    <div class="gauge-panel">
      <div class="grid-bg"></div>
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>
      
      <div class="panel-header">
        <h2 class="panel-title">{{ currentMode === 'download' ? '下载速度' : '上传速度' }}</h2>
        <div class="panel-icon" @click="toggleMode">
          <i :class="currentMode === 'download' ? 'fas fa-download' : 'fas fa-upload'"></i>
        </div>
      </div>
      
      <div class="gauge-container">
        <div class="gauge">
          <div class="gauge-body">
            <div 
              class="gauge-fill" 
              :style="{ transform: `rotate(${currentAngle / 180}turn)` }"
            ></div>
            <div 
              class="gauge-pointer" 
              :style="{ transform: `translateX(-50%) rotate(${currentAngle}deg)` }"
            ></div>
          </div>
          <div class="gauge-cover">
            <div class="speed-value">{{ currentSpeedValue.toFixed(1) }}</div>
            <div class="speed-unit">Mbps</div>
          </div>
        </div>
      </div>
      
      <div class="speed-info">
        <div class="info-item">
          <div>峰值</div>
          <div class="info-value">{{ currentPeakValue.toFixed(1) }} Mbps</div>
        </div>
        <div class="info-item">
          <div>平均</div>
          <div class="info-value">{{ currentAvgValue.toFixed(1) }} Mbps</div>
        </div>
        <div class="info-item">
          <div>{{ currentMode === 'download' ? '延迟' : '波动' }}</div>
          <div class="info-value">
            {{ currentMode === 'download' ? `${currentLatency} ms` : `${currentJitter} ms` }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 网络状态面板 -->
    <div class="network-status">
      <div class="status-item">
        <div class="status-title">IP地址</div>
        <div class="status-value">{{ ipAddress }}</div>
      </div>
      <div class="status-item">
        <div class="status-title">连接类型</div>
        <div class="status-value">{{ connectionType }}</div>
      </div>
      <div class="status-item">
        <div class="status-title">信号强度</div>
        <div class="status-value">{{ signalStrength }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

export default {
  name: 'NetworkSpeedGauge',
  setup() {
    // 当前显示模式 (download/upload)
    const currentMode = ref('download');
    
    // 速度数据
    const speedData = ref({
      download: {
        value: 0,
        peak: 0,
        avg: 0,
        sum: 0,
        latency: 0,
        color: '#00b4ff'
      },
      upload: {
        value: 0,
        peak: 0,
        avg: 0,
        sum: 0,
        jitter: 0,
        color: '#ff7675'
      }
    });
    
    const dataCount = ref(0);
    const updateInterval = ref(null);
    const networkInfoInterval = ref(null);
    
    // 网络信息
    const ipAddress = ref('192.168.1.100');
    const connectionType = ref('5G');
    const signalStrength = ref('-75 dBm');
    
    // 计算属性
    const currentSpeedValue = computed(() => speedData.value[currentMode.value].value);
    const currentPeakValue = computed(() => speedData.value[currentMode.value].peak);
    const currentAvgValue = computed(() => speedData.value[currentMode.value].avg);
    const currentLatency = computed(() => speedData.value.download.latency);
    const currentJitter = computed(() => speedData.value.upload.jitter);
    const currentAngle = computed(() => {
      const maxValue = currentMode.value === 'download' ? 200 : 100;
      const percentage = Math.min(currentSpeedValue.value / maxValue, 1);
      return percentage * 180;
    });
    
    // 切换显示模式
    const toggleMode = () => {
      currentMode.value = currentMode.value === 'download' ? 'upload' : 'download';
    };
    
    // 更新数据
    const updateData = () => {
      // 更新下载速度
      speedData.value.download.value = Math.max(0, 
        speedData.value.download.value + (Math.random() - 0.45) * 40
      );
      speedData.value.download.value = Math.min(speedData.value.download.value, 220);
      
      // 更新上传速度
      speedData.value.upload.value = Math.max(0, 
        speedData.value.upload.value + (Math.random() - 0.5) * 20
      );
      speedData.value.upload.value = Math.min(speedData.value.upload.value, 110);
      
      // 更新峰值
      speedData.value.download.peak = Math.max(speedData.value.download.peak, speedData.value.download.value);
      speedData.value.upload.peak = Math.max(speedData.value.upload.peak, speedData.value.upload.value);
      
      // 更新平均值
      speedData.value.download.sum += speedData.value.download.value;
      speedData.value.upload.sum += speedData.value.upload.value;
      dataCount.value++;
      
      speedData.value.download.avg = speedData.value.download.sum / dataCount.value;
      speedData.value.upload.avg = speedData.value.upload.sum / dataCount.value;
      
      // 更新延迟和抖动
      speedData.value.download.latency = 
        Math.max(1, Math.floor(50 - speedData.value.download.value / 6 + Math.random() * 10));
      
      speedData.value.upload.jitter = Math.floor(1 + Math.random() * 5);
    };
    
    // 模拟IP地址和网络信息
    const simulateNetworkInfo = () => {
      const types = ['5G', '4G LTE', 'Wi-Fi 6', '光纤'];
      const strengthValues = ['-65 dBm', '-75 dBm', '-85 dBm', '-95 dBm'];
      
      connectionType.value = types[Math.floor(Math.random() * types.length)];
      signalStrength.value = strengthValues[Math.floor(Math.random() * strengthValues.length)];
    };
    
    // 初始化数据
    const initData = () => {
      for (let i = 0; i < 5; i++) {
        setTimeout(updateData, i * 300);
      }
    };
    
    // 生命周期钩子
    onMounted(() => {
      initData();
      simulateNetworkInfo();
      updateInterval.value = setInterval(updateData, 1000);
      networkInfoInterval.value = setInterval(simulateNetworkInfo, 10000);
    });
    
    onBeforeUnmount(() => {
      if (updateInterval.value) clearInterval(updateInterval.value);
      if (networkInfoInterval.value) clearInterval(networkInfoInterval.value);
    });
    
    return {
      currentMode,
      currentSpeedValue,
      currentPeakValue,
      currentAvgValue,
      currentLatency,
      currentJitter,
      currentAngle,
      ipAddress,
      connectionType,
      signalStrength,
      toggleMode
    };
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard {
  width: 90%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.gauge-panel {
  background: linear-gradient(145deg, rgba(16, 22, 40, 0.8), rgba(8, 12, 25, 0.9));
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 180, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.gauge-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00b4ff, transparent);
  animation: scanline 3s linear infinite;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
  z-index: 2;
}

.panel-title {
  font-size: 24px;
  font-weight: 300;
  color: #00f2fe;
  text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.panel-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(0, 180, 255, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(0, 180, 255, 0.3);
  box-shadow: 0 0 15px rgba(0, 180, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.panel-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(0, 180, 255, 0.4);
}

.panel-icon i {
  font-size: 24px;
  color: #00b4ff;
}

.gauge-container {
  width: 100%;
  height: 250px;
  position: relative;
  margin: 20px 0;
}

.gauge {
  position: relative;
  width: 100%;
  height: 100%;
}

.gauge-body {
  width: 100%;
  height: 0;
  padding-bottom: 50%;
  position: relative;
  border-top-left-radius: 100% 200%;
  border-top-right-radius: 100% 200%;
  overflow: hidden;
  background: #0d1424;
  border: 2px solid rgba(0, 180, 255, 0.3);
}

.gauge-fill {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #00b4ff, #00f2fe);
  transform-origin: center top;
  transform: rotate(0.5turn);
  transition: transform 1s ease-out;
}

.gauge-cover {
  width: 75%;
  height: 150%;
  background: #0a0e17;
  border-radius: 50%;
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5) inset;
}

.speed-value {
  font-size: 48px;
  font-weight: 300;
  line-height: 1;
}

.speed-unit {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 5px;
}

.gauge-pointer {
  position: absolute;
  width: 4px;
  height: 40%;
  background: #ff4757;
  left: 50%;
  bottom: 50%;
  transform-origin: bottom center;
  transform: translateX(-50%) rotate(0.5turn);
  z-index: 10;
  transition: transform 1s ease-out;
  box-shadow: 0 0 10px rgba(255, 71, 87, 0.7);
}

.gauge-pointer::before {
  content: '';
  position: absolute;
  width: 15px;
  height: 15px;
  background: #ff4757;
  border-radius: 50%;
  bottom: -7px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 10px rgba(255, 71, 87, 0.7);
}

.speed-info {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.info-item {
  text-align: center;
  flex: 1;
}

.info-value {
  font-size: 18px;
  color: #fff;
  margin-top: 5px;
}

.network-status {
  background: linear-gradient(145deg, rgba(16, 22, 40, 0.8), rgba(8, 12, 25, 0.9));
  border-radius: 20px;
  padding: 20px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 180, 255, 0.2);
}

.status-item {
  text-align: center;
  flex: 1;
}

.status-title {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin-bottom: 5px;
}

.status-value {
  font-size: 18px;
  color: #00f2fe;
}

.grid-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.05;
  background-image: 
    linear-gradient(rgba(0, 180, 255, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 180, 255, 0.3) 1px, transparent 1px);
  background-size: 20px 20px;
  z-index: 1;
}

.corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border-color: #00b4ff;
  border-style: solid;
  border-width: 0;
}

.corner-tl {
  top: 10px;
  left: 10px;
  border-top-width: 2px;
  border-left-width: 2px;
}

.corner-tr {
  top: 10px;
  right: 10px;
  border-top-width: 2px;
  border-right-width: 2px;
}

.corner-bl {
  bottom: 10px;
  left: 10px;
  border-bottom-width: 2px;
  border-left-width: 2px;
}

.corner-br {
  bottom: 10px;
  right: 10px;
  border-bottom-width: 2px;
  border-right-width: 2px;
}

@keyframes scanline {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard {
    width: 95%;
    padding: 20px 0;
  }
  
  .network-status {
    flex-direction: column;
    gap: 15px;
  }
  
  .panel-title {
    font-size: 20px;
  }
  
  .speed-value {
    font-size: 36px;
  }
  
  .gauge-container {
    height: 200px;
  }
}
</style>
```

## 使用组件示例

```vue
<template>
  <div class="app">
    <NetworkSpeedGauge />
  </div>
</template>

<script>
import NetworkSpeedGauge from './components/NetworkSpeedGauge.vue';

export default {
  name: 'App',
  components: {
    NetworkSpeedGauge
  }
};
</script>

<style>
body {
  background-color: #0a0e17;
  color: #fff;
  font-family: 'Arial', sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  margin: 0;
  padding: 20px;
}

.app {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
```

## 组件特点

1. **完整的Vue 3组件**：使用Composition API实现
2. **响应式设计**：适配不同屏幕尺寸
3. **动画效果**：保留了原HTML中的所有动画效果
4. **数据管理**：使用ref和computed管理组件状态
5. **生命周期管理**：正确清理定时器
6. **类型安全**：虽然使用了JavaScript，但结构清晰易于转换为TypeScript

## 转换为TypeScript版本

如需TypeScript版本，只需：
1. 将文件重命名为`.vue.ts`
2. 添加类型定义
3. 使用`defineComponent`和接口定义props和state

这个组件保留了原始HTML中的所有功能和视觉效果，同时提供了更好的可维护性和可重用性。
