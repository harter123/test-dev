import {get_code, put_code, post_code} from "./common";
const user_path = 'backend/user/';
export const register = function (name, pwd) {
  return post_code(user_path, {username: name, password: pwd})
};

export const login = function (name, pwd) {
  return put_code(user_path, {username: name, password: pwd})
};

export const get_user = function () {
  return get_code(user_path);
};
