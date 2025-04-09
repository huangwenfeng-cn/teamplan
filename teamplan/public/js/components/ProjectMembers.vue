<template>
  <div class="project-members">
    <div class="section-header">
      <h2>项目成员</h2>  <!-- 原文: Project Members -->
      <Button
        v-if="canAddMembers"
        icon="user-plus"
        secondary
        @click="showAddMemberDialog = true"
      >
        添加成员  <!-- 原文: Add Member -->
      </Button>
    </div>
    
    <div v-if="loading" class="loading-state">
      <p>加载�?..</p>  <!-- 原文: Loading... -->
    </div>
    
    <div v-else-if="members.length === 0" class="empty-state">
      <p>该项目暂无成�?/p>  <!-- 原文: No members in this project -->
    </div>
    
    <div v-else class="members-list">
      <div
        v-for="member in members"
        :key="member.name"
        class="member-item"
      >
        <div class="member-info">
          <UserAvatar
            :user="member.full_name || member.name"
            :image-url="member.image"
            :size="40"
          />
          <div class="member-details">
            <div class="member-name">{{ member.full_name || member.name }}</div>
            <div class="member-email">{{ member.email }}</div>
          </div>
        </div>
        
        <div class="member-role">
          <select
            v-if="canManageMembers && member.name !== currentUser.name"
            v-model="member.role"
            @change="updateMemberRole(member)"
          >
            <option value="Member">成员</option>  <!-- 原文: Member -->
            <option value="Admin">管理�?/option>  <!-- 原文: Admin -->
          </select>
          <span v-else>{{ member.role === 'Admin' ? '管理�? : '成员' }}</span>  <!-- 原文: Admin / Member -->
        </div>
        
        <div class="member-actions">
          <button
            v-if="canManageMembers && member.name !== currentUser.name"
            class="remove-button"
            @click="confirmRemoveMember(member)"
          >
            <i class="icon icon-x"></i>
            <span>移除</span>  <!-- 原文: Remove -->
          </button>
        </div>
      </div>
    </div>
    
    <Dialog
      v-model="showAddMemberDialog"
      title="添加成员"  <!-- 原文: Add Member -->
    >
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="搜索用户..."  <!-- 原文: Search users... -->
        />
      </div>
      
      <div v-if="searchResults.length === 0" class="empty-search">
        <p>未找到用�?/p>  <!-- 原文: No users found -->
      </div>
      
      <div v-else class="search-results">
        <div
          v-for="user in searchResults"
          :key="user.name"
          class="user-item"
          :class="{ 'is-member': isMember(user) }"
        >
          <div class="user-info">
            <UserAvatar
              :user="user.full_name || user.name"
              :image-url="user.image"
              :size="32"
            />
            <div class="user-details">
              <div class="user-name">{{ user.full_name || user.name }}</div>
              <div class="user-email">{{ user.email }}</div>
            </div>
          </div>
          
          <Button
            v-if="!isMember(user)"
            @click="addMember(user)"
          >
            添加  <!-- 原文: Add -->
          </Button>
          <span v-else class="already-member">已是成员</span>  <!-- 原文: Already a member -->
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import UserAvatar from './UserAvatar.vue';
import Button from './Button.vue';
import Dialog from './Dialog.vue';

export default {
  components: {
    UserAvatar,
    Button,
    Dialog
  },
  props: {
    projectId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const members = ref([]);
    const loading = ref(true);
    const availableUsers = ref([]);
    const currentUser = ref('');
    
    // 对话框状�?
    const showAddMemberDialog = ref(false);
    const showEditMemberDialog = ref(false);
    const showRemoveMemberDialog = ref(false);
    
    // 表单数据
    const newMember = ref({
      user: '',
      role: ''
    });
    const editingMember = ref(null);
    const memberToRemove = ref(null);
    
    // 角色列表
    const roles = [
      { value: 'admin', label: '管理�? },  // 原文: Admin
      { value: 'member', label: '成员' },  // 原文: Member
      { value: 'guest', label: '访客' }  // 原文: Guest
    ];
    
    // 权限检�?
    const canAddMembers = computed(() => {
      // 这里可以根据实际需求实现权限检�?
      return true;
    });
    
    const canManageMembers = computed(() => {
      // 这里可以根据实际需求实现权限检�?
      return true;
    });
    
    // 方法
    function getRoleName(role) {
      const roleObj = roles.find(r => r.value === role);
      return roleObj ? roleObj.label : role;
    }
    
    async function fetchMembers() {
      loading.value = true;
      try {
        // 这里应该调用API获取项目成员
        // 示例数据
        members.value = [
          {
            user: 'admin',
            full_name: '管理�?,
            role: 'admin',
            image: ''
          },
          {
            user: 'user1',
            full_name: '用户1',
            role: 'member',
            image: ''
          }
        ];
        
        currentUser.value = 'admin'; // 当前登录用户
      } catch (error) {
        console.error('获取项目成员失败:', error);
      } finally {
        loading.value = false;
      }
    }
    
    async function fetchAvailableUsers() {
      try {
        // 这里应该调用API获取可用用户
        // 示例数据
        availableUsers.value = [
          { name: 'user2', full_name: '用户2' },
          { name: 'user3', full_name: '用户3' }
        ];
      } catch (error) {
        console.error('获取可用用户失败:', error);
      }
    }
    
    function editMember(member) {
      editingMember.value = { ...member };
      showEditMemberDialog.value = true;
    }
    
    function removeMember(member) {
      memberToRemove.value = member;
      showRemoveMemberDialog.value = true;
    }
    
    async function addMember() {
      try {
        // 这里应该调用API添加项目成员
        console.log('添加成员:', newMember.value);
        
        // 模拟添加成功
        const user = availableUsers.value.find(u => u.name === newMember.value.user);
        members.value.push({
          user: newMember.value.user,
          full_name: user ? user.full_name : newMember.value.user,
          role: newMember.value.role,
          image: ''
        });
        
        showAddMemberDialog.value = false;
        
        // 重置表单
        newMember.value = {
          user: '',
          role: ''
        };
        
        // 刷新成员列表
        fetchMembers();
        fetchAvailableUsers();
      } catch (error) {
        console.error('添加成员失败:', error);
      }
    }
    
    async function updateMember() {
      if (!editingMember.value) return;
      
      try {
        // 这里应该调用API更新项目成员
        console.log('更新成员:', editingMember.value);
        
        // 模拟更新成功
        const index = members.value.findIndex(m => m.user === editingMember.value.user);
        if (index !== -1) {
          members.value[index].role = editingMember.value.role;
        }
        
        showEditMemberDialog.value = false;
        editingMember.value = null;
        
        // 刷新成员列表
        fetchMembers();
      } catch (error) {
        console.error('更新成员失败:', error);
      }
    }
    
    async function confirmRemoveMember() {
      if (!memberToRemove.value) return;
      
      try {
        // 这里应该调用API移除项目成员
        console.log('移除成员:', memberToRemove.value);
        
        // 模拟移除成功
        members.value = members.value.filter(m => m.user !== memberToRemove.value.user);
        
        showRemoveMemberDialog.value = false;
        memberToRemove.value = null;
        
        // 刷新成员列表
        fetchMembers();
        fetchAvailableUsers();
      } catch (error) {
        console.error('移除成员失败:', error);
      }
    }
    
    // 初始�?
    fetchMembers();
    fetchAvailableUsers();
    
    return {
      members,
      loading,
      availableUsers,
      currentUser,
      showAddMemberDialog,
      showEditMemberDialog,
      showRemoveMemberDialog,
      newMember,
      editingMember,
      memberToRemove,
      roles,
      canAddMembers,
      canManageMembers,
      getRoleName,
      editMember,
      removeMember,
      addMember,
      updateMember,
      confirmRemoveMember
    };
  }
}
</script>

<style scoped>
.project-members {
  margin-bottom: 2rem;
}

.members-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.members-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.loading-state,
.empty-state {
  padding: 2rem 0;
  text-align: center;
  color: #a0aec0;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.member-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
}

.member-info {
  display: flex;
  align-items: center;
}

.member-details {
  margin-left: 0.75rem;
}

.member-name {
  font-weight: 500;
  color: #2d3748;
}

.member-role {
  font-size: 0.875rem;
  color: #718096;
}

.member-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
