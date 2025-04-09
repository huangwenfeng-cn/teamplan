<template>
  <div class="file-upload">
    <div
      class="upload-area"
      :class="{ 'is-dragging': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        class="file-input"
        :multiple="multiple"
        :accept="accept"
        @change="handleFileChange"
      />
      
      <div class="upload-icon">
        <i class="icon icon-upload"></i>
      </div>
      
      <div class="upload-text">
        <p class="primary-text">
          拖放文件到此处或点击上传  <!-- 原文: Drop files here or click to upload -->
        </p>
        <p class="secondary-text" v-if="maxFileSize">
          最大文件大�? {{ formatFileSize(maxFileSize) }}  <!-- 原文: Maximum file size: -->
        </p>
      </div>
    </div>
    
    <div v-if="files.length > 0" class="file-list">
      <div
        v-for="(file, index) in files"
        :key="index"
        class="file-item"
      >
        <div class="file-icon">
          <i :class="getFileIcon(file.type)"></i>
        </div>
        
        <div class="file-info">
          <div class="file-name">{{ file.name }}</div>
          <div class="file-size">{{ formatFileSize(file.size) }}</div>
        </div>
        
        <div class="file-status">
          <div v-if="file.status === 'uploading'" class="upload-progress">
            <div
              class="progress-bar"
              :style="{ width: `${file.progress}%` }"
            ></div>
            <span class="progress-text">{{ file.progress }}%</span>
          </div>
          
          <div v-else-if="file.status === 'success'" class="upload-success">
            <i class="icon icon-check"></i>
            <span>上传成功</span>  <!-- 原文: Uploaded -->
          </div>
          
          <div v-else-if="file.status === 'error'" class="upload-error">
            <i class="icon icon-alert-circle"></i>
            <span>{{ file.error || '上传失败' }}</span>  <!-- 原文: Upload failed -->
          </div>
        </div>
        
        <button
          class="remove-button"
          @click="removeFile(index)"
        >
          <i class="icon icon-x"></i>
        </button>
      </div>
    </div>
    
    <div class="upload-actions" v-if="files.length > 0 && !autoUpload">
      <Button
        @click="uploadFiles"
        :disabled="isUploading"
        :loading="isUploading"
      >
        上传文件  <!-- 原文: Upload Files -->
      </Button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import Button from './Button.vue';

export default {
  components: {
    Button
  },
  props: {
    multiple: {
      type: Boolean,
      default: false
    },
    accept: {
      type: String,
      default: ''
    },
    maxFileSize: {
      type: Number,
      default: 0 // 单位: 字节
    },
    autoUpload: {
      type: Boolean,
      default: false
    },
    uploadUrl: {
      type: String,
      default: ''
    }
  },
  emits: ['upload', 'success', 'error'],
  setup(props, { emit }) {
    const fileInput = ref(null);
    const files = ref([]);
    const isDragging = ref(false);
    const isUploading = ref(false);
    
    // 触发文件选择
    function triggerFileInput() {
      fileInput.value.click();
    }
    
    // 处理文件选择
    function handleFileChange(event) {
      const selectedFiles = Array.from(event.target.files);
      addFiles(selectedFiles);
      
      // 重置文件输入，以便可以再次选择相同的文�?
      event.target.value = null;
    }
    
    // 处理文件拖放
    function handleDrop(event) {
      isDragging.value = false;
      const droppedFiles = Array.from(event.dataTransfer.files);
      addFiles(droppedFiles);
    }
    
    // 添加文件
    function addFiles(newFiles) {
      // 检查文件大�?
      const validFiles = newFiles.filter(file => {
        if (props.maxFileSize && file.size > props.maxFileSize) {
          console.warn(`文件 "${file.name}" 超过最大大小限制`);
          return false;
        }
        return true;
      });
      
      // 如果不允许多文件，则替换现有文件
      if (!props.multiple) {
        files.value = validFiles.map(file => ({
          file,
          name: file.name,
          size: file.size,
          type: file.type,
          status: 'pending',
          progress: 0,
          error: null
        }));
      } else {
        // 添加到现有文件列�?
        const newFileObjects = validFiles.map(file => ({
          file,
          name: file.name,
          size: file.size,
          type: file.type,
          status: 'pending',
          progress: 0,
          error: null
        }));
        
        files.value = [...files.value, ...newFileObjects];
      }
      
      // 如果设置了自动上传，则立即上�?
      if (props.autoUpload && validFiles.length > 0) {
        uploadFiles();
      }
    }
    
    // 移除文件
    function removeFile(index) {
      files.value.splice(index, 1);
    }
    
    // 上传文件
    async function uploadFiles() {
      if (files.value.length === 0 || isUploading.value) return;
      
      isUploading.value = true;
      
      // 获取待上传的文件
      const pendingFiles = files.value.filter(file => file.status !== 'success');
      
      // 通知父组件开始上�?
      emit('upload', pendingFiles.map(file => file.file));
      
      // 如果没有提供上传URL，则由父组件处理上传
      if (!props.uploadUrl) {
        isUploading.value = false;
        return;
      }
      
      // 上传每个文件
      for (let i = 0; i < pendingFiles.length; i++) {
        const fileObj = pendingFiles[i];
        const formData = new FormData();
        formData.append('file', fileObj.file);
        
        try {
          // 更新状态为上传�?
          const fileIndex = files.value.findIndex(f => f.name === fileObj.name);
          if (fileIndex !== -1) {
            files.value[fileIndex].status = 'uploading';
          }
          
          // 创建上传请求
          const xhr = new XMLHttpRequest();
          
          // 监听上传进度
          xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
              const progress = Math.round((event.loaded / event.total) * 100);
              const fileIndex = files.value.findIndex(f => f.name === fileObj.name);
              if (fileIndex !== -1) {
                files.value[fileIndex].progress = progress;
              }
            }
          });
          
          // 等待上传完成
          await new Promise((resolve, reject) => {
            xhr.onload = () => {
              if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response);
              } else {
                reject(new Error(`上传失败: ${xhr.statusText}`));
              }
            };
            
            xhr.onerror = () => reject(new Error('网络错误'));
            
            xhr.open('POST', props.uploadUrl);
            xhr.send(formData);
          });
          
          // 更新状态为成功
          const successIndex = files.value.findIndex(f => f.name === fileObj.name);
          if (successIndex !== -1) {
            files.value[successIndex].status = 'success';
          }
          
          // 通知父组件上传成�?
          emit('success', fileObj.file);
        } catch (error) {
          console.error('文件上传失败:', error);
          
          // 更新状态为错误
          const errorIndex = files.value.findIndex(f => f.name === fileObj.name);
          if (errorIndex !== -1) {
            files.value[errorIndex].status = 'error';
            files.value[errorIndex].error = error.message;
          }
          
          // 通知父组件上传失�?
          emit('error', { file: fileObj.file, error });
        }
      }
      
      isUploading.value = false;
    }
    
    // 获取文件图标
    function getFileIcon(fileType) {
      if (fileType.startsWith('image/')) {
        return 'icon icon-image';
      } else if (fileType.startsWith('video/')) {
        return 'icon icon-film';
      } else if (fileType.startsWith('audio/')) {
        return 'icon icon-music';
      } else if (fileType === 'application/pdf') {
        return 'icon icon-file-text';
      } else if (fileType.includes('spreadsheet') || fileType.includes('excel')) {
        return 'icon icon-file-text';
      } else if (fileType.includes('document') || fileType.includes('word')) {
        return 'icon icon-file-text';
      } else if (fileType.includes('presentation') || fileType.includes('powerpoint')) {
        return 'icon icon-file-text';
      } else {
        return 'icon icon-file';
      }
    }
    
    // 格式化文件大�?
    function formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    return {
      fileInput,
      files,
      isDragging,
      isUploading,
      triggerFileInput,
      handleFileChange,
      handleDrop,
      removeFile,
      uploadFiles,
      getFileIcon,
      formatFileSize
    };
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.upload-area {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  border: 2px dashed #e2e8f0;
  border-radius: 0.5rem;
  background-color: #f7fafc;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: #cbd5e0;
}

.upload-area.is-dragging {
  border-color: #4299e1;
  background-color: #ebf8ff;
}

.file-input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}

.upload-icon {
  font-size: 2rem;
  color: #a0aec0;
  margin-bottom: 1rem;
}

.upload-text {
  text-align: center;
}

.primary-text {
  margin: 0 0 0.5rem;
  font-weight: 500;
  color: #4a5568;
}

.secondary-text {
  margin: 0;
  font-size: 0.875rem;
  color: #a0aec0;
}

.file-list {
  margin-top: 1rem;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.file-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
  color: #4a5568;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
  word-break: break-all;
}

.file-size {
  font-size: 0.75rem;
  color: #a0aec0;
}

.file-status {
  margin: 0 1rem;
  min-width: 100px;
}

.upload-progress {
  position: relative;
  height: 0.5rem;
  background-color: #edf2f7;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #4299e1;
  transition: width 0.2s;
}

.progress-text {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 0.75rem;
  color: #4a5568;
}

.upload-success {
  display: flex;
  align-items: center;
  color: #48bb78;
  font-size: 0.875rem;
}

.upload-error {
  display: flex;
  align-items: center;
  color: #f56565;
  font-size: 0.875rem;
}

.upload-success .icon,
.upload-error .icon {
  margin-right: 0.25rem;
}

.remove-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
}

.remove-button:hover {
  color: #f56565;
}

.upload-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}
</style>
