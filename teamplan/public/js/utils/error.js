/**
 * 处理API错误并返回用户友好的错误消息
 * @param {Error} error - 捕获的错误对�?
 * @returns {string} 用户友好的错误消�?
 */
export function handleApiError(error) {
  if (!error.response) {
    return '无法连接到服务器，请检查您的网络连接�?;  // 原文: Could not connect to server, please check your network connection.
  }
  
  const { status, data } = error.response;
  
  switch (status) {
    case 400:
      return data.message || '请求无效，请检查您的输入�?;  // 原文: Invalid request, please check your input.
    case 401:
      return '您的会话已过期，请重新登录�?;  // 原文: Your session has expired, please login again.
    case 403:
      return '您没有权限执行此操作�?;  // 原文: You don't have permission to perform this action.
    case 404:
      return '请求的资源不存在�?;  // 原文: The requested resource does not exist.
    case 500:
      return '服务器错误，请稍后再试�?;  // 原文: Server error, please try again later.
    default:
      return data.message || '发生未知错误，请稍后再试�?;  // 原文: An unknown error occurred, please try again later.
  }
}

/**
 * 显示错误通知
 * @param {string} message - 错误消息
 */
export function showErrorNotification(message) {
  // 这里可以集成您的通知系统
  console.error('错误:', message);  // 原文: Error:
  
  // 如果使用 toast 通知系统
  if (window.showToast) {
    window.showToast({
      message,
      type: 'error',
      duration: 5000
    });
  }
}
