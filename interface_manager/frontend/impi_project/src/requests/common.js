import VueCookies from "vue-cookies";

export const host = 'http://127.0.0.1/';

export const post_code = function (url, params) {
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

export const put_code = function (url, params) {
  let body = JSON.stringify(params);
  return fetch(host + url, {
    method: 'PUT',
    body: body,
    credentials: "include",
    headers: {
      'token': VueCookies.get( 'token'),
    }
  }).then(response => {
    return response.json()
  })
};

export const delete_code = function (url, params) {
  let body = JSON.stringify(params);
  return fetch(host + url, {
    method: 'DELETE',
    body: body,
    credentials: "include",
    headers: {
      'token': VueCookies.get( 'token'),
    }
  }).then(response => {
    return response.json()
  })
};


export const get_code = function (url) {
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
