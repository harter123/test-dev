import {get_code, put_code, post_code, delete_code} from "./common";

const service_path = 'backend/mocks/';
// 获取服务的树形结构
export const get_mocks = function () {
  return get_code(service_path)
};
// 创建mock
export const create_mock = function (data) {
  return post_code(service_path, data)
};

// 更新mock
export const update_mock = function (mock_id, data) {
  return put_code(service_path + mock_id, data)
};

// 删除mock
export const delete_mock = function (mock_id) {
  return delete_code(service_path + mock_id)
};

