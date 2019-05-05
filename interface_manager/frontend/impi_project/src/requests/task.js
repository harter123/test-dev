import {get_code, put_code, post_code, delete_code} from "./common";

const task_path = 'backend/tasks/';
// 获取任务列表
export const get_tasks = function () {
  return get_code(task_path)
};

// 获取任务列表
export const get_task = function (task_id) {
  return get_code(task_path + task_id);
};

// 创建任务
export const create_task = function (name, description) {
  return post_code(task_path, {name: name, description: description})
};

// 更新任务
export const update_task = function (task_id, name, description) {
  return put_code(task_path + task_id, {name: name, description: description,})
};

// 删除任务
export const delete_task = function (task_id) {
  return delete_code(task_path + task_id)
};

// 任务获取接口列表
export const task_get_interfaces = function (task_id) {
  return get_code(task_path + task_id + "/interfaces")
};
// 任务添加接口
export const task_add_interfaces = function (task_id, data) {
  return post_code(task_path + task_id + "/interfaces", data)
};
// 任务移除接口
export const task_delete_interface = function (task_id, data) {
  return delete_code(task_path + task_id + "/interfaces", data)
};

// 任务获取结果列表
export const task_get_versions = function (task_id) {
  return get_code(task_path + task_id + "/versions")
};

// 任务获取历史列表
export const task_get_version_results = function (version_id) {
  return get_code(task_path + "versions/" + version_id + '/results')
};

// 执行任务
export const run_task = function (task_id, data) {
  return post_code(task_path + task_id + '/run', data)
};

// 停止任务
export const stop_task = function (task_id) {
  return delete_task(task_path + task_id + '/run');
};
