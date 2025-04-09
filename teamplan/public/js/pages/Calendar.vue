<template>
  <div class="calendar-page">
    <PageHeader>
      <h1>日历</h1>  <!-- 原文: Calendar -->
      <template #actions>
        <Button
          icon="plus"
          @click="showNewEventDialog = true"
        >
          新建事件  <!-- 原文: New Event -->
        </Button>
      </template>
    </PageHeader>
    
    <div class="calendar-controls">
      <div class="calendar-navigation">
        <Button
          icon="chevron-left"
          @click="previousMonth"
        >
          上个月 <!-- 原文: Previous Month -->
        </Button>
        <h2 class="current-month">{{ currentMonthName }} {{ currentYear }}</h2>
        <Button
          icon="chevron-right"
          @click="nextMonth"
        >
          下个月 <!-- 原文: Next Month -->
        </Button>
      </div>
      
      <div class="view-options">
        <Button
          :class="{ active: viewMode === 'month' }"
          @click="viewMode = 'month'"
        >
          月视图 <!-- 原文: Month View -->
        </Button>
        <Button
          :class="{ active: viewMode === 'week' }"
          @click="viewMode = 'week'"
        >
          周视图 <!-- 原文: Week View -->
        </Button>
        <Button
          :class="{ active: viewMode === 'day' }"
          @click="viewMode = 'day'"
        >
          日视图 <!-- 原文: Day View -->
        </Button>
      </div>
    </div>
    
    <div class="calendar-container">
      <div v-if="viewMode === 'month'" class="month-view">
        <div class="weekday-headers">
          <div
            v-for="(day, index) in weekdays"
            :key="index"
            class="weekday-header"
          >
            {{ day }}
          </div>
        </div>
        
        <div class="calendar-grid">
          <div
            v-for="(day, index) in calendarDays"
            :key="index"
            class="calendar-day"
            :class="{
              'current-month': day.currentMonth,
              'today': day.isToday,
              'has-events': day.events.length > 0
            }"
            @click="selectDay(day)"
          >
            <div class="day-number">{{ day.date }}</div>
            <div v-if="day.events.length > 0" class="day-events">
              <div
                v-for="(event, eventIndex) in day.events.slice(0, 2)"
                :key="eventIndex"
                class="day-event"
                :style="{ backgroundColor: event.color || '#4299e1' }"
                @click.stop="viewEvent(event)"
              >
                {{ event.title }}
              </div>
              <div
                v-if="day.events.length > 2"
                class="more-events"
                @click.stop="viewAllDayEvents(day)"
              >
                还有 {{ day.events.length - 2 }} 个事件 <!-- 原文: +X more -->
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="viewMode === 'week'" class="week-view">
        <div class="weekday-headers">
          <div class="time-column-header"></div>
          <div
            v-for="(day, index) in weekDays"
            :key="index"
            class="weekday-header"
            :class="{ 'today': day.isToday }"
          >
            <div class="weekday-name">{{ day.dayName }}</div>
            <div class="weekday-date">{{ day.date }}</div>
          </div>
        </div>
        
        <div class="week-grid">
          <div class="time-column">
            <div
              v-for="hour in 24"
              :key="hour"
              class="time-slot"
            >
              {{ hour - 1 }}:00
            </div>
          </div>
          
          <div
            v-for="(day, dayIndex) in weekDays"
            :key="dayIndex"
            class="day-column"
          >
            <div
              v-for="hour in 24"
              :key="hour"
              class="hour-slot"
            >
              <div
                v-for="(event, eventIndex) in getEventsForHour(day, hour - 1)"
                :key="eventIndex"
                class="week-event"
                :style="{ backgroundColor: event.color || '#4299e1' }"
                @click="viewEvent(event)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="viewMode === 'day'" class="day-view">
        <div class="day-header">
          <h3>{{ selectedDayName }} {{ selectedDayDate }}</h3>
        </div>
        
        <div class="day-grid">
          <div class="time-column">
            <div
              v-for="hour in 24"
              :key="hour"
              class="time-slot"
            >
              {{ hour - 1 }}:00
            </div>
          </div>
          
          <div class="events-column">
            <div
              v-for="hour in 24"
              :key="hour"
              class="hour-slot"
            >
              <div
                v-for="(event, eventIndex) in getEventsForHour(selectedDay, hour - 1)"
                :key="eventIndex"
                class="day-event"
                :style="{ backgroundColor: event.color || '#4299e1' }"
                @click="viewEvent(event)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 新建事件对话框 -->
    <Dialog
      v-model="showNewEventDialog"
      title="创建新事件"  <!-- 原文: Create New Event -->
    >
      <div class="mb-4">
        <label for="event-title" class="block mb-1">事件标题</label>  <!-- 原文: Event Title -->
        <input
          id="event-title"
          v-model="newEvent.title"
          class="w-full"
          placeholder="输入事件标题..."  <!-- 原文: Enter event title... -->
        />
      </div>
      <div class="mb-4">
        <label for="event-description" class="block mb-1">事件描述 (可选)</label>  <!-- 原文: Event Description (optional) -->
        <textarea
          id="event-description"
          v-model="newEvent.description"
          class="w-full"
          placeholder="输入事件描述..."  <!-- 原文: Enter event description... -->
          rows="3"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="event-date" class="block mb-1">日期</label>  <!-- 原文: Date -->
        <input
          id="event-date"
          v-model="newEvent.date"
          type="date"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="event-time" class="block mb-1">时间 (可选)</label>  <!-- 原文: Time (optional) -->
        <input
          id="event-time"
          v-model="newEvent.time"
          type="time"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="event-project" class="block mb-1">项目 (可选)</label>  <!-- 原文: Project (optional) -->
        <select
          id="event-project"
          v-model="newEvent.project"
          class="w-full"
        >
          <option value="">无项目</option>  <!-- 原文: No Project -->
          <option
            v-for="project in projects"
            :key="project.name"
            :value="project.name"
          >
            {{ project.title }}
          </option>
        </select>
      </div>
      <template #actions>
        <Button secondary @click="showNewEventDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!newEvent.title || !newEvent.date"
          @click="createEvent"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 查看事件对话框 -->
    <Dialog
      v-if="selectedEvent"
      v-model="showEventDialog"
      :title="selectedEvent.title"
    >
      <div class="event-details">
        <div v-if="selectedEvent.description" class="mb-4">
          <h4>描述</h4>  <!-- 原文: Description -->
          <p>{{ selectedEvent.description }}</p>
        </div>
        
        <div class="mb-4">
          <h4>日期和时间</h4>  <!-- 原文: Date & Time -->
          <p>
            {{ formatDate(selectedEvent.date) }}
            <span v-if="selectedEvent.time">{{ formatTime(selectedEvent.time) }}</span>
          </p>
        </div>
        
        <div v-if="selectedEvent.project" class="mb-4">
          <h4>项目</h4>  <!-- 原文: Project -->
          <p>{{ selectedEvent.project }}</p>
        </div>
        
        <div class="mb-4">
          <h4>创建者</h4>  <!-- 原文: Created By -->
          <p>{{ selectedEvent.owner }}</p>
        </div>
      </div>
      
      <template #actions>
        <Button secondary @click="showEventDialog = false">
          关闭  <!-- 原文: Close -->
        </Button>
        <Button
          v-if="canEditEvent(selectedEvent)"
          @click="editEvent"
        >
          编辑  <!-- 原文: Edit -->
        </Button>
        <Button
          v-if="canDeleteEvent(selectedEvent)"
          secondary
          class="text-red-500"
          @click="confirmDeleteEvent"
        >
          删除  <!-- 原文: Delete -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 编辑事件对话框 -->
    <Dialog
      v-if="editingEvent"
      v-model="showEditEventDialog"
      title="编辑事件"  <!-- 原文: Edit Event -->
    >
      <div class="mb-4">
        <label for="edit-event-title" class="block mb-1">事件标题</label>  <!-- 原文: Event Title -->
        <input
          id="edit-event-title"
          v-model="editingEvent.title"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="edit-event-description" class="block mb-1">事件描述</label>  <!-- 原文: Event Description -->
        <textarea
          id="edit-event-description"
          v-model="editingEvent.description"
          class="w-full"
          rows="3"
        ></textarea>
      </div>
      <div class="mb-4">
        <label for="edit-event-date" class="block mb-1">日期</label>  <!-- 原文: Date -->
        <input
          id="edit-event-date"
          v-model="editingEvent.date"
          type="date"
          class="w-full"
        />
      </div>
      <div class="mb-4">
        <label for="edit-event-time" class="block mb-1">时间</label>  <!-- 原文: Time -->
        <input
          id="edit-event-time"
          v-model="editingEvent.time"
          type="time"
          class="w-full"
        />
      </div>
      <template #actions>
        <Button secondary @click="showEditEventDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :disabled="!editingEvent.title || !editingEvent.date"
          @click="updateEvent"
        >
          保存  <!-- 原文: Save -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 确认删除对话框 -->
    <Dialog
      v-model="showDeleteConfirmDialog"
      title="确认删除"  <!-- 原文: Confirm Delete -->
    >
      <p>您确定要删除此事件吗？此操作无法撤销。</p>  <!-- 原文: Are you sure you want to delete this event? This action cannot be undone. -->
      
      <template #actions>
        <Button secondary @click="showDeleteConfirmDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          class="text-red-500"
          @click="deleteEvent"
        >
          删除  <!-- 原文: Delete -->
        </Button>
      </template>
    </Dialog>
    
    <!-- 日期事件列表对话框 -->
    <Dialog
      v-if="selectedDay"
      v-model="showDayEventsDialog"
      :title="`${formatDate(selectedDay.fullDate)} 的事件`"  <!-- 原文: Events for [date] -->
    >
      <div v-if="selectedDay.events.length === 0" class="empty-state">
        <p>这一天没有事件</p>  <!-- 原文: No events for this day -->
      </div>
      
      <div v-else class="day-events-list">
        <div
          v-for="(event, index) in selectedDay.events"
          :key="index"
          class="day-event-item"
          @click="viewEvent(event)"
        >
          <div class="event-time">
            {{ event.time ? formatTime(event.time) : '全天' }}  <!-- 原文: All day -->
          </div>
          <div class="event-title">{{ event.title }}</div>
        </div>
      </div>
      
      <template #actions>
        <Button @click="showDayEventsDialog = false">
          关闭  <!-- 原文: Close -->
        </Button>
        <Button
          icon="plus"
          @click="createEventForDay"
        >
          添加事件  <!-- 原文: Add Event -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { formatDate, formatTime } from '../utils/date';
import { handleApiError } from '../utils/error';

export default {
  setup() {
    const router = useRouter();
    
    // 状态变量
    const currentDate = ref(new Date());
    const viewMode = ref('month');
    const events = ref([]);
    const loading = ref(false);
    const projects = ref([]);
    
    // 对话框状态
    const showNewEventDialog = ref(false);
    const showEventDialog = ref(false);
    const showEditEventDialog = ref(false);
    const showDeleteConfirmDialog = ref(false);
    const showDayEventsDialog = ref(false);
    
    // 选中的事件和日期
    const selectedEvent = ref(null);
    const selectedDay = ref(null);
    const editingEvent = ref(null);
    
    // 新事件表单
    const newEvent = ref({
      title: '',
      description: '',
      date: '',
      time: '',
      project: ''
    });
    
    // 计算属性
    const currentYear = computed(() => currentDate.value.getFullYear());
    const currentMonth = computed(() => currentDate.value.getMonth());
    
    const currentMonthName = computed(() => {
      const monthNames = [
        '一月', '二月', '三月', '四月', '五月', '六月',
        '七月', '八月', '九月', '十月', '十一月', '十二月'
      ];
      return monthNames[currentMonth.value];
    });
    
    const weekdays = computed(() => {
      return ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    });
    
    const calendarDays = computed(() => {
      const year = currentYear.value;
      const month = currentMonth.value;
      
      // 获取当月第一天
      const firstDay = new Date(year, month, 1);
      // 获取当月最后一天
      const lastDay = new Date(year, month + 1, 0);
      
      // 获取当月第一天是星期几
      const firstDayOfWeek = firstDay.getDay();
      
      // 获取上个月的最后几天
      const prevMonthLastDay = new Date(year, month, 0).getDate();
      
      const days = [];
      
      // 添加上个月的日期
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const day = prevMonthLastDay - i;
        const date = new Date(year, month - 1, day);
        days.push({
          date: day,
          fullDate: date.toISOString().split('T')[0],
          currentMonth: false,
          isToday: isToday(date),
          events: getEventsForDay(date)
        });
      }
      
      // 添加当月的日期
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(year, month, i);
        days.push({
          date: i,
          fullDate: date.toISOString().split('T')[0],
          currentMonth: true,
          isToday: isToday(date),
          events: getEventsForDay(date)
        });
      }
      
      // 添加下个月的日期
      const remainingDays = 42 - days.length; // 6行7列 = 42
      for (let i = 1; i <= remainingDays; i++) {
        const date = new Date(year, month + 1, i);
        days.push({
          date: i,
          fullDate: date.toISOString().split('T')[0],
          currentMonth: false,
          isToday: isToday(date),
          events: getEventsForDay(date)
        });
      }
      
      return days;
    });
    
    const weekDays = computed(() => {
      const days = [];
      const today = new Date();
      
      // 获取本周的第一天（周日）
      const firstDayOfWeek = new Date(today);
      const day = today.getDay();
      firstDayOfWeek.setDate(today.getDate() - day);
      
      // 生成一周的日期
      for (let i = 0; i < 7; i++) {
        const date = new Date(firstDayOfWeek);
        date.setDate(firstDayOfWeek.getDate() + i);
        
        days.push({
          date: date.getDate(),
          fullDate: date.toISOString().split('T')[0],
          dayName: weekdays.value[i],
          isToday: isToday(date),
          events: getEventsForDay(date)
        });
      }
      
      return days;
    });
    
    const selectedDayName = computed(() => {
      if (!selectedDay.value) return '';
      const date = new Date(selectedDay.value.fullDate);
      return weekdays.value[date.getDay()];
    });
    
    const selectedDayDate = computed(() => {
      if (!selectedDay.value) return '';
      return formatDate(selectedDay.value.fullDate);
    });
    
    // 方法
    function isToday(date) {
      const today = new Date();
      return date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear();
    }
    
    function getEventsForDay(date) {
      if (!events.value.length) return [];
      
      const dateStr = date.toISOString().split('T')[0];
      return events.value.filter(event => event.date === dateStr);
    }
    
    function getEventsForHour(day, hour) {
      if (!day || !day.events.length) return [];
      
      return day.events.filter(event => {
        if (!event.time) return false;
        const eventHour = parseInt(event.time.split(':')[0]);
        return eventHour === hour;
      });
    }
    
    function previousMonth() {
      const date = new Date(currentDate.value);
      date.setMonth(date.getMonth() - 1);
      currentDate.value = date;
    }
    
    function nextMonth() {
      const date = new Date(currentDate.value);
      date.setMonth(date.getMonth() + 1);
      currentDate.value = date;
    }
    
    function selectDay(day) {
      selectedDay.value = day;
      showDayEventsDialog.value = true;
    }
    
    function viewEvent(event) {
      selectedEvent.value = event;
      showEventDialog.value = true;
      
      if (showDayEventsDialog.value) {
        showDayEventsDialog.value = false;
      }
    }
    
    function viewAllDayEvents(day) {
      selectedDay.value = day;
      showDayEventsDialog.value = true;
    }
    
    function createEventForDay() {
      if (!selectedDay.value) return;
      
      newEvent.value = {
        title: '',
        description: '',
        date: selectedDay.value.fullDate,
        time: '',
        project: ''
      };
      
      showDayEventsDialog.value = false;
      showNewEventDialog.value = true;
    }
    
    function editEvent() {
      if (!selectedEvent.value) return;
      
      editingEvent.value = { ...selectedEvent.value };
      showEventDialog.value = false;
      showEditEventDialog.value = true;
    }
    
    function confirmDeleteEvent() {
      showDeleteConfirmDialog.value = true;
    }
    
    function canEditEvent(event) {
      // 检查用户是否有权限编辑事件
      // 这里可以根据实际需求实现
      return true;
    }
    
    function canDeleteEvent(event) {
      // 检查用户是否有权限删除事件
      // 这里可以根据实际需求实现
      return true;
    }
    
    async function fetchEvents() {
      loading.value = true;
      try {
        // 这里应该调用API获取事件数据
        // 示例数据
        events.value = [
          {
            name: 'event1',
            title: '团队会议',
            description: '讨论项目进度',
            date: '2023-05-15',
            time: '10:00',
            project: '项目A',
            owner: '张三',
            color: '#4299e1'
          },
          {
            name: 'event2',
            title: '客户演示',
            description: '向客户展示最新功能',
            date: '2023-05-18',
            time: '14:30',
            project: '项目B',
            owner: '李四',
            color: '#48bb78'
          }
        ];
      } catch (error) {
        console.error('获取事件失败:', error);
      } finally {
        loading.value = false;
      }
    }
    
    async function fetchProjects() {
      try {
        // 这里应该调用API获取项目数据
        // 示例数据
        projects.value = [
          { name: 'project1', title: '项目A' },
          { name: 'project2', title: '项目B' }
        ];
      } catch (error) {
        console.error('获取项目失败:', error);
      }
    }
    
    async function createEvent() {
      try {
        // 这里应该调用API创建事件
        console.log('创建事件:', newEvent.value);
        
        // 模拟创建成功
        const createdEvent = {
          name: `event${Date.now()}`,
          ...newEvent.value,
          owner: '当前用户'
        };
        
        events.value.push(createdEvent);
        showNewEventDialog.value = false;
        
        // 重置表单
        newEvent.value = {
          title: '',
          description: '',
          date: '',
          time: '',
          project: ''
        };
        
        // 刷新日历
        fetchEvents();
      } catch (error) {
        console.error('创建事件失败:', error);
      }
    }
    
    async function updateEvent() {
      if (!editingEvent.value) return;
      
      try {
        // 这里应该调用API更新事件
        console.log('更新事件:', editingEvent.value);
        
        // 模拟更新成功
        const index = events.value.findIndex(e => e.name === editingEvent.value.name);
        if (index !== -1) {
          events.value[index] = { ...editingEvent.value };
        }
        
        showEditEventDialog.value = false;
        editingEvent.value = null;
        
        // 刷新日历
        fetchEvents();
      } catch (error) {
        console.error('更新事件失败:', error);
      }
    }
    
    async function deleteEvent() {
      if (!selectedEvent.value) return;
      
      try {
        // 这里应该调用API删除事件
        console.log('删除事件:', selectedEvent.value);
        
        // 模拟删除成功
        events.value = events.value.filter(e => e.name !== selectedEvent.value.name);
        
        showDeleteConfirmDialog.value = false;
        showEventDialog.value = false;
        selectedEvent.value = null;
        
        // 刷新日历
        fetchEvents();
      } catch (error) {
        console.error('删除事件失败:', error);
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      fetchEvents();
      fetchProjects();
    });
    
    return {
      currentDate,
      currentYear,
      currentMonth,
      currentMonthName,
      viewMode,
      weekdays,
      calendarDays,
      weekDays,
      selectedDay,
      selectedDayName,
      selectedDayDate,
      events,
      loading,
      projects,
      showNewEventDialog,
      showEventDialog,
      showEditEventDialog,
      showDeleteConfirmDialog,
      showDayEventsDialog,
      selectedEvent,
      editingEvent,
      newEvent,
      previousMonth,
      nextMonth,
      selectDay,
      viewEvent,
      viewAllDayEvents,
      createEventForDay,
      editEvent,
      confirmDeleteEvent,
      canEditEvent,
      canDeleteEvent,
      createEvent,
      updateEvent,
      deleteEvent,
      getEventsForHour,
      formatDate,
      formatTime
    };
  }
};
</script>