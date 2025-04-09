/**
 * 验证电子邮箱格式
 * @param {string} email - 要验证的电子邮箱
 * @returns {boolean} 是否有效
 */
export function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

/**
 * 验证密码强度
 * @param {string} password - 要验证的密码
 * @returns {object} 包含验证结果和消息的对象
 */
export function validatePassword(password) {
  if (!password) {
    return {
      valid: false,
      message: '密码不能为空'  // 原文: Password cannot be empty
    };
  }
  
  if (password.length < 8) {
    return {
      valid: false,
      message: '密码长度必须至少�?个字�?  // 原文: Password must be at least 8 characters long
    };
  }
  
  // 检查是否包含至少一个数�?
  if (!/\d/.test(password)) {
    return {
      valid: false,
      message: '密码必须包含至少一个数�?  // 原文: Password must contain at least one number
    };
  }
  
  // 检查是否包含至少一个字�?
  if (!/[a-zA-Z]/.test(password)) {
    return {
      valid: false,
      message: '密码必须包含至少一个字�?  // 原文: Password must contain at least one letter
    };
  }
  
  return {
    valid: true,
    message: '密码有效'  // 原文: Password is valid
  };
}

/**
 * 验证表单字段
 * @param {object} fields - 要验证的字段对象
 * @param {object} rules - 验证规则
 * @returns {object} 包含验证结果和错误消息的对象
 */
export function validateForm(fields, rules) {
  const errors = {};
  let isValid = true;
  
  for (const field in rules) {
    const value = fields[field];
    const fieldRules = rules[field];
    
    if (fieldRules.required && !value) {
      errors[field] = `${fieldRules.label || field}是必填项`;  // 原文: is required
      isValid = false;
      continue;
    }
    
    if (fieldRules.email && value && !validateEmail(value)) {
      errors[field] = `请输入有效的电子邮箱地址`;  // 原文: Please enter a valid email address
      isValid = false;
      continue;
    }
    
    if (fieldRules.minLength && value && value.length < fieldRules.minLength) {
      errors[field] = `${fieldRules.label || field}长度必须至少�?{fieldRules.minLength}个字符`;  // 原文: must be at least X characters long
      isValid = false;
      continue;
    }
    
    if (fieldRules.match && value !== fields[fieldRules.match]) {
      errors[field] = `${fieldRules.label || field}�?{rules[fieldRules.match].label || fieldRules.match}不匹配`;  // 原文: does not match
      isValid = false;
      continue;
    }
  }
  
  return {
    isValid,
    errors
  };
}
