<template>
    <div class="date-picker">
      <div class="date-input-container">
        <input
          type="text"
          class="date-input"
          :placeholder="placeholder"
          :value="formattedDate"
          readonly
          @click="toggleCalendar"
        />
        <button
          v-if="modelValue && clearable"
          class="clear-button"
          @click.stop="clearDate"
        >
          <i class="icon icon-x"></i>
        </button>
        <button class="calendar-button" @click.stop="toggleCalendar">
          <i class="icon icon-calendar"></i>
        </button>
      </div>
      
      <div v-if="showCalendar" class="calendar-container">
        <div class="calendar-header">
          <button class="nav-button" @click="prevMonth">
            <i class="icon icon-chevron-left"></i>
          </button>
          <div class="current-month">
            {{ currentMonthName }} {{ currentYear }}
          </div>
          <button class="nav-button" @click="nextMonth">
            <i class="icon icon-chevron-right"></i>
          </button>
        </div>
        
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
              'is-selected': day.isSelected
            }"
            @click="selectDate(day)"
          >
            {{ day.day }}
          </div>
        </div>
        
        <div class="calendar-footer">
          <button class="today-button" @click="goToToday">
            今天
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
  import { formatDate } from '../utils/date';
  
  export default {
    props: {
      modelValue: {
        type: String,
        default: ''
      },
      placeholder: {
        type: String,
        default: '选择日期'
      },
      clearable: {
        type: Boolean,
        default: true
      },
      format: {
        type: String,
        default: 'YYYY-MM-DD'
      }
    },
    emits: ['update:modelValue'],
    setup(props, { emit }) {
      const showCalendar = ref(false);
      const currentMonth = ref(new Date().getMonth());
      const currentYear = ref(new Date().getFullYear());
      
      // 星期几的本地�?
      const weekdays = ['�?, '一', '�?, '�?, '�?, '�?, '�?];
      
      // 月份名称的本地化
      const monthNames = [
        '一�?, '二月', '三月', '四月', '五月', '六月',
        '七月', '八月', '九月', '十月', '十一�?, '十二�?
      ];
      
      const currentMonthName = computed(() => {
        return monthNames[currentMonth.value];
      });
      
      const formattedDate = computed(() => {
        if (!props.modelValue) return '';
        
        try {
          const date = new Date(props.modelValue);
          return formatDate(date);
        } catch (error) {
          return '';
        }
      });
      
      const calendarDays = computed(() => {
        const days = [];
        
        // 获取当前月的第一�?
        const firstDay = new Date(currentYear.value, currentMonth.value, 1);
        
        // 获取当前月的最后一�?
        const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
        
        // 获取当前月第一天是星期�?
        const firstDayOfWeek = firstDay.getDay();
        
        // 获取上个月的最后几�?
        const prevMonthLastDay = new Date(currentYear.value, currentMonth.value, 0).getDate();
        
        // 填充上个月的日期
        for (let i = firstDayOfWeek - 1; i >= 0; i--) {
          const day = prevMonthLastDay - i;
          const date = new Date(currentYear.value, currentMonth.value - 1, day);
          
          days.push({
            day,
            date,
            otherMonth: true,
            isToday: isToday(date),
            isSelected: isSelectedDate(date)
          });
        }
        
        // 填充当前月的日期
        for (let i = 1; i <= lastDay.getDate(); i++) {
          const date = new Date(currentYear.value, currentMonth.value, i);
          
          days.push({
            day: i,
            date,
            otherMonth: false,
            isToday: isToday(date),
            isSelected: isSelectedDate(date)
          });
        }
        
        // 填充下个月的日期
        const remainingDays = 42 - days.length; // 6�?�?= 42
        for (let i = 1; i <= remainingDays; i++) {
          const date = new Date(currentYear.value, currentMonth.value + 1, i);
          
          days.push({
            day: i,
            date,
            otherMonth: true,
            isToday: isToday(date),
            isSelected: isSelectedDate(date)
          });
        }
        
        return days;
      });
      
      function isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
          date.getMonth() === today.getMonth() &&
          date.getFullYear() === today.getFullYear();
      }
      
      function isSelectedDate(date) {
        if (!props.modelValue) return false;
        
        try {
          const selectedDate = new Date(props.modelValue);
          return date.getDate() === selectedDate.getDate() &&
            date.getMonth() === selectedDate.getMonth() &&
            date.getFullYear() === selectedDate.getFullYear();
        } catch (error) {
          return false;
        }
      }
      
      function toggleCalendar() {
        showCalendar.value = !showCalendar.value;
      }
      
      function prevMonth() {
        if (currentMonth.value === 0) {
          currentMonth.value = 11;
          currentYear.value--;
        } else {
          currentMonth.value--;
        }
      }
      
      function nextMonth() {
        if (currentMonth.value === 11) {
          currentMonth.value = 0;
          currentYear.value++;
        } else {
          currentMonth.value++;
        }
      }
      
      function goToToday() {
        const today = new Date();
        currentMonth.value = today.getMonth();
        currentYear.value = today.getFullYear();
      }
      
      function selectDate(day) {
        const date = day.date;
        
        // 如果选择的是其他月份的日期，切换到对应月�?
        if (day.otherMonth) {
          currentMonth.value = date.getMonth();
          currentYear.value = date.getFullYear();
        }
        
        // 格式化日期为 YYYY-MM-DD
        const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        
        emit('update:modelValue', formattedDate);
        showCalendar.value = false;
      }
      
      function clearDate() {
        emit('update:modelValue', '');
      }
      
      function handleClickOutside(event) {
        if (showCalendar.value && !event.target.closest('.date-picker')) {
          showCalendar.value = false;
        }
      }
      
      onMounted(() => {
        document.addEventListener('click', handleClickOutside);
        
        // 如果有初始日期，设置日历到对应月�?
        if (props.modelValue) {
          try {
            const date = new Date(props.modelValue);
            currentMonth.value = date.getMonth();
            currentYear.value = date.getFullYear();
          } catch (error) {
            // 忽略无效日期
          }
        }
      });
      
      onBeforeUnmount(() => {
        document.removeEventListener('click', handleClickOutside);
      });
      
      return {
        showCalendar,
        currentMonth,
        currentYear,
        weekdays,
        currentMonthName,
        formattedDate,
        calendarDays,
        toggleCalendar,
        prevMonth,
        nextMonth,
        goToToday,
        selectDate,
        clearDate
      };
    }
  }
  </script>
  
  <style scoped>
  .date-picker {
    position: relative;
    width: 100%;
  }
  
  .date-input-container {
    display: flex;
    align-items: center;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    padding: 0.5rem;
  }
  
  .date-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 0.875rem;
  }
  
  .clear-button,
  .calendar-button {
    background: none;
    border: none;
    color: #a0aec0;
    cursor: pointer;
    padding: 0.25rem;
  }
  
  .calendar-container {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 10;
    width: 300px;
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin-top: 0.5rem;
  }
  
  .calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .current-month {
    font-weight: 500;
    color: #2d3748;
  }
  
  .nav-button {
    background: none;
    border: none;
    color: #4a5568;
    cursor: pointer;
    padding: 0.25rem;
  }
  
  .weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .weekday {
    font-size: 0.75rem;
    color: #718096;
    font-weight: 500;
  }
  
  .days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: repeat(6, 1fr);
    text-align: center;
  }
  
  .day {
    padding: 0.5rem;
    cursor: pointer;
    border-radius: 0.25rem;
    transition: background-color 0.2s;
  }
  
  .day:hover {
    background-color: #f7fafc;
  }
  
  .day.is-other-month {
    color: #cbd5e0;
  }
  
  .day.is-today {
    font-weight: 600;
    color: #4299e1;
  }
  
  .day.is-selected {
    background-color: #4299e1;
    color: white;
  }
  
  .day.is-selected:hover {
    background-color: #3182ce;
  }
  
  .calendar-footer {
    padding: 0.75rem;
    text-align: center;
    border-top: 1px solid #e2e8f0;
  }
  
  .today-button {
    background: none;
    border: none;
    color: #4299e1;
    cursor: pointer;
    font-size: 0.875rem;
  }
  </style>
