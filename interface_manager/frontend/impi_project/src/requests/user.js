import VueCookies from 'vue-cookies'

let host = 'http://127.0.0.1:8000/';

let post_code = function (url, params) {
  let body = JSON.stringify(params);
  return fetch(host + url, {
    method: 'POST',
    body: body,
    credentials: "include",
    headers: {
      'token': VueCookies.get( 'token'),
    }
  }).then(response => {
    return response.json()
  })
};

let get_code = function (url) {
  return fetch(host + url, {
    method: 'GET',
    credentials: "include",
    headers: {
      'token': VueCookies.get( 'token'),
    }
  }).then(response => {
    return response.json()
  })
};

export const register = function (name, pwd) {
  return post_code('backend/user/register', {name: name, pwd: pwd})
};

export const login = function (name, pwd) {
  return post_code('backend/user/login', {name: name, pwd: pwd})
};

export const get_user = function () {
  return get_code('backend/user/get');
};
