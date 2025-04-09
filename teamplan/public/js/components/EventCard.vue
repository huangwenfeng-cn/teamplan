<template>
  <div class="event-card" :style="{ borderLeftColor: event.color || '#4299e1' }">
    <div class="event-header">
      <h3 class="event-title">{{ event.title }}</h3>
    </div>
    
    <div class="event-meta">
      <div class="meta-item date">
        <i class="icon icon-calendar"></i>
        <span>{{ formatDate(event.date) }}</span>
      </div>
      
      <div v-if="event.time" class="meta-item time">
        <i class="icon icon-clock"></i>
        <span>{{ formatTime(event.time) }}</span>
      </div>
      
      <div v-if="event.project" class="meta-item project">
        <i class="icon icon-folder"></i>
        <span>{{ event.project }}</span>
      </div>
    </div>
    
    <div v-if="event.description" class="event-description">
      <p>{{ event.description }}</p>
    </div>
  </div>
</template>

<script>
import { formatDate, formatTime } from '../utils/date';

export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  setup() {
    return {
      formatDate,
      formatTime
    };
  }
}
</script>

<style scoped>
.event-card {
  border: 1px solid #e2e8f0;
  border-left-width: 4px;
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.event-header {
  margin-bottom: 0.5rem;
}

.event-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.event-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: #718096;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item .icon {
  margin-right: 0.25rem;
}

.event-description {
  font-size: 0.875rem;
  color: #4a5568;
  line-height: 1.5;
}

.event-description p {
  margin: 0;
}
</style>
