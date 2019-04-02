import {put_code, post_code, delete_code, get_code} from "./common";

const service_path = 'backend/interfaces/';

// 创建接口
export const create_interface = function (data) {
  return post_code(service_path, data);
};

// 更新接口
export const update_interface = function (interface_id, data) {
  return put_code(service_path + interface_id, data)
};

// 删除接口
export const delete_interface = function (interface_id) {
  return delete_code(service_path + interface_id);
};

// 获取接口
export const get_interface = function (interface_id) {
  return get_code(service_path + interface_id);
};

