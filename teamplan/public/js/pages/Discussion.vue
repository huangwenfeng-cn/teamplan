<template>
  <div class="discussion-page">
    <PageHeader>
      <h1>讨论</h1>  <!-- 原文: Discussion -->
      <template #actions>
        <Button
          v-if="canCreateDiscussion"
          icon="plus"
          @click="showNewDiscussionDialog = true"
        >
          新讨论 <!-- 原文: New Discussion -->
        </Button>
      </template>
    </PageHeader>
    
    <Dialog
      v-model="showNewDiscussionDialog"
      title="创建新讨论"  <!-- 原文: Add New Discussion -->
    >
      <div class="mb-4">
        <label for="discussion-title" class="block mb-1">讨论标题</label> <!-- 原文: Discussion Title -->
        <input
          id="discussion-title"
          v-model="newDiscussionTitle"
          class="w-full"
          placeholder="输入讨论标题..." <!-- 原文: Enter discussion title... -->
        />
      </div>
      <div>
        <label for="discussion-content" class="block mb-1">讨论内容</label> <!-- 原文: Discussion Content -->
        <textarea
          id="discussion-content"
          v-model="newDiscussionContent"
          class="w-full"
          placeholder="输入讨论内容..." <!-- 原文: Enter discussion content... -->
          rows="5"
        ></textarea>
      </div>
      <template #actions>
        <Button secondary @click="showNewDiscussionDialog = false">
          取消  <!-- 原文: Cancel -->
        </Button>
        <Button
          :loading="creatingDiscussion"
          :disabled="!newDiscussionTitle || !newDiscussionContent"
          @click="createDiscussion"
        >
          创建  <!-- 原文: Create -->
        </Button>
      </template>
    </Dialog>
  </div>
</template>