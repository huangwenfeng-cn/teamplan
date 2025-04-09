<template>
    <div class="calendar-component">
      <div class="calendar-header">
        <div class="header-left">
          <Button
            icon="chevron-left"
            secondary
            size="small"
            @click="prevMonth"
          />
          <Button
            icon="chevron-right"
            secondary
            size="small"
            @click="nextMonth"
          />
          <Button
            secondary
            size="small"
            @click="goToToday"
          >
            今天
          </Button>
        </div>
        
        <div class="current-month">
          {{ currentMonthName }} {{ currentYear }}
        </div>
        
        <div class="header-right">
          <div class="view-selector">
            <Button
              secondary
              size="small"
              :class="{ 'is-active': view === 'month' }"
              @click="view = 'month'"
            >
              �?
            </Button>
            <Button
              secondary
              size="small"
              :class="{ 'is-active': view === 'week' }"
              @click="view = 'week'"
            >
              �?
            </Button>
            <Button
              secondary
              size="small"
              :class="{ 'is-active': view === 'day' }"
              @click="view = 'day'"
            >
              �?
            </Button>
          </div>
        </div>
      </div>
      
      <div v-if="view === 'month'" class="month-view">
        <div class="weekdays">
          <div v-for="day in weekdays" :key="day" class="weekday">
            {{ day }}
          </div>
        </div>
        
        <div class="days">
          <div
            v-for="(day, index) in calendarDays"
            :key="index"
            class="day"
            :class="{
              'is-other-month': day.otherMonth,
              'is-today': day.isToday,
              'is-selected': day.isSelected,
              'has-events': day.events.length > 0
            }"
            @click="selectDate(day.date)"
          >
            <div class="day-header">
              <span class="day-number">{{ day.day }}</span>
            </div>
            
            <div class="day-events">
              <div
                v-for="(event, eventIndex) in day.events.slice(0, 3)"
                :key="eventIndex"
                class="event"
                :style="{ backgroundColor: event.color || '#4299e1' }"
                @click.stop="showEventDetails(event)"
              >
                {{ event.title }}
              </div>
              
              <div
                v-if="day.events.length > 3"
                class="more-events"
                @click.stop="showMoreEvents(day)"
              >
                还有 {{ day.events.length - 3 }} �?
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="view === 'week'" class="week-view">
        <div class="week-header">
          <div class="time-column"></div>
          <div
            v-for="(day, index) in weekDays"
            :key="index"
            class="day-column-header"
            :class="{ 'is-today': day.isToday }"
          >
            <div class="day-name">{{ weekdays[day.date.getDay()] }}</div>
            <div class="day-number">{{ day.day }}</div>
          </div>
        </div>
        
        <div class="week-body">
          <div class="time-slots">
            <div
              v-for="hour in 24"
              :key="hour"
              class="time-slot"
            >
              <div class="time-label">{{ formatHour(hour - 1) }}</div>
              <div class="hour-grid"></div>
            </div>
          </div>
          
          <div class="day-columns">
            <div
              v-for="(day, dayIndex) in weekDays"
              :key="dayIndex"
              class="day-column"
              :class="{ 'is-today': day.isToday }"
            >
              <div
                v-for="event in day.events"
                :key="event.id"
                class="week-event"
                :style="{
                  top: `${calculateEventTop(event)}px`,
                  height: `${calculateEventHeight(event)}px`,
                  backgroundColor: event.color || '#4299e1'
                }"
                @click="showEventDetails(event)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="view === 'day'" class="day-view">
        <div class="day-header">
          <div class="day-title">
            {{ formatDate(selectedDate) }}
          </div>
        </div>
        
        <div class="day-body">
          <div class="time-slots">
            <div
              v-for="hour in 24"
              :key="hour"
              class="time-slot"
            >
              <div class="time-label">{{ formatHour(hour - 1) }}</div>
              <div class="hour-grid"></div>
            </div>
          </div>
          
          <div class="events-column">
            <div
              v-for="event in selectedDateEvents"
              :key="event.id"
              class="day-event"
              :style="{
                top: `${calculateEventTop(event)}px`,
                height: `${calculateEventHeight(event)}px`,
                backgroundColor: event.color || '#4299e1'
              }"
              @click="showEventDetails(event)"
            >
              <div class="event-time">
                {{ formatEventTime(event) }}
              </div>
              <div class="event-title">
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <Dialog
        v-model="showEventModal"
        :title="selectedEvent ? '事件详情' : '添加事件'"
      >
        <div v-if="selectedEvent" class="event-details">
          <h3>{{ selectedEvent.title }}</h3>
          
          <div class="detail-item">
            <div class="detail-label">时间</div>
            <div class="detail-value">
              {{ formatEventDateTime(selectedEvent) }}
            </div>
          </div>
          
          <div v-if="selectedEvent.location" class="detail-item">
            <div class="detail-label">地点</div>
            <div class="detail-value">
              {{ selectedEvent.location }}
            </div>
          </div>
          
          <div v-if="selectedEvent.description" class="detail-item">
            <div class="detail-label">描述</div>
            <div class="detail-value">
              {{ selectedEvent.description }}
            </div>
          </div>
          
          <div class="event-actions">
            <Button
              icon="edit"
              secondary
              @click="editEvent"
            >
              编辑
            </Button>
            
            <Button
              icon="trash"
              secondary
              @click="confirmDeleteEvent"
            >
              删除
            </Button>
          </div>
        </div>
        
        <form v-else @submit.prevent="saveEvent" class="event-form">
          <div class="form-group">
            <label for="event-title">标题</label>
            <input
              id="event-title"
              v-model="eventForm.title"
              type="text"
              required
            />
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="event-start-date">开始日�?/label>
              <DatePicker
                id="event-start-date"
                v-model="eventForm.startDate"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="event-start-time">开始时�?/label>
              <input
                id="event-start-time"
                v-model="eventForm.startTime"
                type="time"
                required
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="event-end-date">结束日期</label>
              <DatePicker
                id="event-end-date"
                v-model="eventForm.endDate"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="event-end-time">结束时间</label>
              <input
                id="event-end-time"
                v-model="eventForm.endTime"
                type="time"
                required
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="event-location">地点</label>
            <input
              id="event-location"
              v-model="eventForm.location"
              type="text"
            />
          </div>
          
          <div class="form-group">
            <label for="event-description">描述</label>
            <textarea
              id="event-description"
              v-model="eventForm.description"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="event-color">颜色</label>
            <div class="color-picker">
              <div
                v-for="color in availableColors"
                :key="color"
                class="color-option"
                :class="{ 'is-selected': eventForm.color === color }"
                :style="{ backgroundColor: color }"
                @click="eventForm.color = color"
              ></div>
            </div>
          </div>
          
          <div class="form-actions">
            <Button
              secondary
              @click="showEventModal = false"
            >
              取消
            </Button>
            
            <Button
              type="submit"
            >
              保存
            </Button>
          </div>
        </form>
      </Dialog>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch, onMounted } from 'vue';
  import Button from './Button.vue';
  import Dialog from './Dialog.vue';
  import DatePicker from './DatePicker.vue';
  import { formatDate as formatDateUtil } from '../utils/date';
  
  export default {
    components: {
      Button,
      Dialog,
      DatePicker
    },
    props: {
      events: {
        type: Array,
        default: () => []
      }
    },
    emits: ['event-added', 'event-updated', 'event-deleted'],
    setup(props, { emit }) {
      // 状�?
      const view = ref('month');
      const currentDate = ref(new Date());
      const selectedDate = ref(new Date());
      const showEventModal = ref(false);
      const selectedEvent = ref(null);
      const eventForm = ref({
        title: '',
        startDate: new Date(),
        startTime: '09:00',
        endDate: new Date(),
        endTime: '10:00',
        location: '',
        description: '',
        color: '#4299e1'
      });
      
      // 星期几名�?
      const weekdays = ref(['周日', '周一', '周二', '周三', '周四', '周五', '周六']);
      
      // 月份名称
      const monthNames = [
        '一�?, '二月', '三月', '四月', '五月', '六月',
        '七月', '八月', '九月', '十月', '十一�?, '十二�?
      ];
      
      // 可用颜色
      const availableColors = [
        '#4299e1', '#48bb78', '#ed8936', '#e53e3e', '#805ad5',
        '#d53f8c', '#38b2ac', '#ecc94b', '#667eea', '#f56565'
      ];
      
      // 计算当前月份名称
      const currentMonthName = computed(() => {
        return monthNames[currentDate.value.getMonth()];
      });
      
      // 计算当前年份
      const currentYear = computed(() => {
        return currentDate.value.getFullYear();
      });
      
      // 计算日历天数
      const calendarDays = computed(() => {
        const year = currentDate.value.getFullYear();
        const month = currentDate.value.getMonth();
        
        // 当月第一�?
        const firstDay = new Date(year, month, 1);
        // 当月最后一�?
        const lastDay = new Date(year, month + 1, 0);
        
        // 当月第一天是星期�?
        const firstDayOfWeek = firstDay.getDay();
        // 当月天数
        const daysInMonth = lastDay.getDate();
        
        // 上个月最后一�?
        const prevMonthLastDay = new Date(year, month, 0);
        const prevMonthDays = prevMonthLastDay.getDate();
        
        const days = [];
        
        // 添加上个月的天数
        for (let i = firstDayOfWeek - 1; i >= 0; i--) {
          const day = prevMonthDays - i;
          const date = new Date(year, month - 1, day);
          days.push({
            day,
            date,
            otherMonth: true,
            isToday: isSameDay(date, new Date()),
            isSelected: isSameDay(date, selectedDate.value),
            events: getEventsForDate(date)
          });
        }
        
        // 添加当月的天�?
        for (let i = 1; i <= daysInMonth; i++) {
          const date = new Date(year, month, i);
          days.push({
            day: i,
            date,
            otherMonth: false,
            isToday: isSameDay(date, new Date()),
            isSelected: isSameDay(date, selectedDate.value),
            events: getEventsForDate(date)
          });
        }
        
        // 添加下个月的天数
        const remainingDays = 42 - days.length;
        for (let i = 1; i <= remainingDays; i++) {
          const date = new Date(year, month + 1, i);
          days.push({
            day: i,
            date,
            otherMonth: true,
            isToday: isSameDay(date, new Date()),
            isSelected: isSameDay(date, selectedDate.value),
            events: getEventsForDate(date)
          });
        }
        
        return days;
      });
      
      // 计算周视图的天数
      const weekDays = computed(() => {
        const date = new Date(selectedDate.value);
        const day = date.getDay();
        const diff = date.getDate() - day;
        
        const days = [];
        
        for (let i = 0; i < 7; i++) {
          const currentDate = new Date(date);
          currentDate.setDate(diff + i);
          
          days.push({
            day: currentDate.getDate(),
            date: currentDate,
            isToday: isSameDay(currentDate, new Date()),
            events: getEventsForDate(currentDate)
          });
        }
        
        return days;
      });
      
      // 计算选中日期的事�?
      const selectedDateEvents = computed(() => {
        return getEventsForDate(selectedDate.value);
      });
      
      // 检查两个日期是否是同一�?
      function isSameDay(date1, date2) {
        return (
          date1.getFullYear() === date2.getFullYear() &&
          date1.getMonth() === date2.getMonth() &&
          date1.getDate() === date2.getDate()
        );
      }
      
      // 获取指定日期的事�?
      function getEventsForDate(date) {
        return props.events.filter(event => {
          const eventStart = new Date(event.start);
          const eventEnd = new Date(event.end);
          
          // 检查事件是否在指定日期
          return (
            isSameDay(eventStart, date) ||
            isSameDay(eventEnd, date) ||
            (date > eventStart && date < eventEnd)
          );
        });
      }
      
      // 格式化日�?
      function formatDate(date) {
        return formatDateUtil(date, 'YYYY年MM月DD�?);
      }
      
      // 格式化小�?
      function formatHour(hour) {
        return `${hour.toString().padStart(2, '0')}:00`;
      }
      
      // 格式化事件时�?
      function formatEventTime(event) {
        const start = new Date(event.start);
        const end = new Date(event.end);
        
        const startHours = start.getHours().toString().padStart(2, '0');
        const startMinutes = start.getMinutes().toString().padStart(2, '0');
        const endHours = end.getHours().toString().padStart(2, '0');
        const endMinutes = end.getMinutes().toString().padStart(2, '0');
        
        return `${startHours}:${startMinutes} - ${endHours}:${endMinutes}`;
      }
      
      // 格式化事件日期时�?
      function formatEventDateTime(event) {
        const start = new Date(event.start);
        const end = new Date(event.end);
        
        const startDate = formatDateUtil(start, 'YYYY年MM月DD�?);
        const endDate = formatDateUtil(end, 'YYYY年MM月DD�?);
        
        const startTime = `${start.getHours().toString().padStart(2, '0')}:${start.getMinutes().toString().padStart(2, '0')}`;
        const endTime = `${end.getHours().toString().padStart(2, '0')}:${end.getMinutes().toString().padStart(2, '0')}`;
        
        if (isSameDay(start, end)) {
          return `${startDate} ${startTime} - ${endTime}`;
        }
        
        return `${startDate} ${startTime} - ${endDate} ${endTime}`;
      }
      
      // 计算事件顶部位置
      function calculateEventTop(event) {
        const start = new Date(event.start);
        const hours = start.getHours();
        const minutes = start.getMinutes();
        
        // 每小时高度为60px
        return (hours * 60) + minutes;
      }
      
      // 计算事件高度
      function calculateEventHeight(event) {
        const start = new Date(event.start);
        const end = new Date(event.end);
        
        // 计算事件持续时间（分钟）
        const durationMinutes = (end - start) / (1000 * 60);
        
        // 每分钟高度为1px
        return Math.max(30, durationMinutes);
      }
      
      // 上个�?
      function prevMonth() {
        const date = new Date(currentDate.value);
        date.setMonth(date.getMonth() - 1);
        currentDate.value = date;
      }
      
      // 下个�?
      function nextMonth() {
        const date = new Date(currentDate.value);
        date.setMonth(date.getMonth() + 1);
        currentDate.value = date;
      }
      
      // 跳转到今�?
      function goToToday() {
        currentDate.value = new Date();
        selectedDate.value = new Date();
      }
      
      // 选择日期
      function selectDate(date) {
        selectedDate.value = date;
      }
      
      // 显示事件详情
      function showEventDetails(event) {
        selectedEvent.value = event;
        showEventModal.value = true;
      }
      
      // 显示更多事件
      function showMoreEvents(day) {
        selectedDate.value = day.date;
        view.value = 'day';
      }
      
      // 编辑事件
      function editEvent() {
        const event = selectedEvent.value;
        const start = new Date(event.start);
        const end = new Date(event.end);
        
        eventForm.value = {
          id: event.id,
          title: event.title,
          startDate: new Date(start.getFullYear(), start.getMonth(), start.getDate()),
          startTime: `${start.getHours().toString().padStart(2, '0')}:${start.getMinutes().toString().padStart(2, '0')}`,
          endDate: new Date(end.getFullYear(), end.getMonth(), end.getDate()),
          endTime: `${end.getHours().toString().padStart(2, '0')}:${end.getMinutes().toString().padStart(2, '0')}`,
          location: event.location || '',
          description: event.description || '',
          color: event.color || '#4299e1'
        };
        
        selectedEvent.value = null;
      }
      
      // 确认删除事件
      function confirmDeleteEvent() {
        if (confirm('确定要删除这个事件吗�?)) {
          emit('event-deleted', selectedEvent.value);
          showEventModal.value = false;
          selectedEvent.value = null;
        }
      }
      
      // 保存事件
      function saveEvent() {
        const form = eventForm.value;
        
        // 解析开始时�?
        const [startHours, startMinutes] = form.startTime.split(':').map(Number);
        const startDate = new Date(form.startDate);
        startDate.setHours(startHours, startMinutes, 0, 0);
        
        // 解析结束时间
        const [endHours, endMinutes] = form.endTime.split(':').map(Number);
        const endDate = new Date(form.endDate);
        endDate.setHours(endHours, endMinutes, 0, 0);
        
        const event = {
          id: form.id || Date.now().toString(),
          title: form.title,
          start: startDate.toISOString(),
          end: endDate.toISOString(),
          location: form.location,
          description: form.description,
          color: form.color
        };
        
        if (form.id) {
          emit('event-updated', event);
        } else {
          emit('event-added', event);
        }
        
        showEventModal.value = false;
        resetEventForm();
      }
      
      // 重置事件表单
      function resetEventForm() {
        const now = new Date();
        const oneHourLater = new Date(now);
        oneHourLater.setHours(now.getHours() + 1);
        
        eventForm.value = {
          title: '',
          startDate: new Date(now.getFullYear(), now.getMonth(), now.getDate()),
          startTime: `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`,
          endDate: new Date(oneHourLater.getFullYear(), oneHourLater.getMonth(), oneHourLater.getDate()),
          endTime: `${oneHourLater.getHours().toString().padStart(2, '0')}:${oneHourLater.getMinutes().toString().padStart(2, '0')}`,
          location: '',
          description: '',
          color: '#4299e1'
        };
      }
      
      // 监听选中日期变化
      watch(selectedDate, () => {
        // 如果选中的日期不在当前月份，则切换到该月�?
        if (selectedDate.value.getMonth() !== currentDate.value.getMonth() ||
            selectedDate.value.getFullYear() !== currentDate.value.getFullYear()) {
          currentDate.value = new Date(
            selectedDate.value.getFullYear(),
            selectedDate.value.getMonth(),
            1
          );
        }
      });
      
      // 初始�?
      onMounted(() => {
        resetEventForm();
      });
      
      return {
        view,
        currentDate,
        selectedDate,
        showEventModal,
        selectedEvent,
        eventForm,
        weekdays,
        availableColors,
        currentMonthName,
        currentYear,
        calendarDays,
        weekDays,
        selectedDateEvents,
        formatDate,
        formatHour,
        formatEventTime,
        formatEventDateTime,
        calculateEventTop,
        calculateEventHeight,
        prevMonth,
        nextMonth,
        goToToday,
        selectDate,
        showEventDetails,
        showMoreEvents,
        editEvent,
        confirmDeleteEvent,
        saveEvent
      };
    }
  }
  </script>
  
  <style scoped>
  .calendar-component {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .header-left,
  .header-right {
    display: flex;
    gap: 0.5rem;
  }
  
  .current-month {
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  .view-selector {
    display: flex;
    border-radius: 0.25rem;
    overflow: hidden;
  }
  
  .view-selector button {
    border-radius: 0;
  }
  
  .view-selector button.is-active {
    background-color: #4299e1;
    color: white;
  }
  
  /* 月视�?*/
  .month-view {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    font-weight: 600;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .days {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: repeat(6, 1fr);
    border-left: 1px solid #e2e8f0;
  }
  
  .day {
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 0.5rem;
    min-height: 100px;
    display: flex;
    flex-direction: column;
  }
  
  .day.is-other-month {
    background-color: #f7fafc;
    color: #a0aec0;
  }
  
  .day.is-today {
    background-color: #ebf8ff;
  }
  
  .day.is-selected .day-number {
    background-color: #4299e1;
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .day-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .day-events {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    overflow: hidden;
  }
  
  .event {
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: white;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
  }
  
  .more-events {
    font-size: 0.75rem;
    color: #4299e1;
    cursor: pointer;
    text-align: center;
  }
  
  /* 周视�?*/
  .week-view {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .week-header {
    display: grid;
    grid-template-columns: 50px repeat(7, 1fr);
    border-bottom: 1px solid #e2e8f0;
  }
  
  .day-column-header {
    padding: 0.5rem;
    text-align: center;
    border-left: 1px solid #e2e8f0;
  }
  
  .day-column-header.is-today {
    background-color: #ebf8ff;
  }
  
  .day-name {
    font-weight: 600;
  }
  
  .week-body {
    flex: 1;
    display: grid;
    grid-template-columns: 50px repeat(7, 1fr);
    overflow-y: auto;
  }
  
  .time-slots {
    display: flex;
    flex-direction: column;
  }
  
  .time-slot {
    height: 60px;
    position: relative;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .time-label {
    position: absolute;
    top: -0.5rem;
    right: 0.5rem;
    font-size: 0.75rem;
    color: #718096;
  }
  
  .day-columns {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
  }
  
  .day-column {
    position: relative;
    border-left: 1px solid #e2e8f0;
  }
  
  .day-column.is-today {
    background-color: #ebf8ff;
  }
  
  .hour-grid {
    height: 100%;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .week-event {
    position: absolute;
    left: 2px;
    right: 2px;
    padding: 0.25rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    color: white;
    overflow: hidden;
    cursor: pointer;
    z-index: 1;
  }
  
  /* 日视�?*/
  .day-view {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .day-header {
    padding: 1rem;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .day-title {
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  .day-body {
    flex: 1;
    display: grid;
    grid-template-columns: 50px 1fr;
    overflow-y: auto;
  }

  .events-column {
    position: relative;
    border-left: 1px solid #e2e8f0;
  }

  .day-event {
    position: absolute;
    left: 2px;
    right: 2px;
    padding: 0.5rem;
    border-radius: 0.25rem;
    color: white;
    overflow: hidden;
    cursor: pointer;
    z-index: 1;
  }

  .event-time {
    font-size: 0.75rem;
    margin-bottom: 0.25rem;
    opacity: 0.9;
  }

  .event-title {
    font-weight: 500;
  }

  /* 事件详情 */
  .event-details {
    padding: 1rem;
  }

  .event-details h3 {
    margin-top: 0;
    margin-bottom: 1rem;
  }

  .detail-item {
    margin-bottom: 1rem;
  }

  .detail-label {
    font-weight: 500;
    margin-bottom: 0.25rem;
    color: #718096;
  }

  .event-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1.5rem;
  }

  /* 事件表单 */
  .event-form {
    padding: 1rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .form-row .form-group {
    flex: 1;
    margin-bottom: 0;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
  }

  .color-picker {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .color-option {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid transparent;
  }

  .color-option.is-selected {
    border-color: #2d3748;
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1.5rem;
  }
</style>
