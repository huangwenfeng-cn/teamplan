/**
 * 格式化日期为本地格式
 * @param {string} dateString - ISO 格式的日期字符串
 * @returns {string} 格式化后的日�?
 */
export function formatDate(dateString) {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');  // 使用中文日期格式
}

/**
 * 格式化日期和时间为本地格�?
 * @param {string} dateTimeString - ISO 格式的日期时间字符串
 * @returns {string} 格式化后的日期和时间
 */
export function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  
  const date = new Date(dateTimeString);
  return date.toLocaleString('zh-CN');  // 使用中文日期时间格式
}

/**
 * 格式化相对时间（例如�?小时前）
 * @param {string} dateTimeString - ISO 格式的日期时间字符串
 * @returns {string} 相对时间字符�?
 */
export function formatRelativeTime(dateTimeString) {
  if (!dateTimeString) return '';
  
  const date = new Date(dateTimeString);
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  
  if (diffSec < 60) {
    return '刚刚';  // 原文: just now
  } else if (diffMin < 60) {
    return `${diffMin} 分钟前`;  // 原文: minutes ago
  } else if (diffHour < 24) {
    return `${diffHour} 小时前`;  // 原文: hours ago
  } else if (diffDay < 30) {
    return `${diffDay} 天前`;  // 原文: days ago
  } else {
    return formatDate(dateTimeString);
  }
}
