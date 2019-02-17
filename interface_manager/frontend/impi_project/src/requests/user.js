let host = 'http://127.0.0.1:8000/'

let common_code = function (url, params) {
  let body = JSON.stringify(params)
  return fetch(host + url, {
    method: 'POST',
    body: body
  }).then(response => {
    return response.json()
  })
}

export const register = function (name, pwd) {
  return common_code('backend/user/register', {name: name, pwd: pwd})
}

export const login = function (name, pwd) {
  return common_code('backend/user/login', {name: name, pwd: pwd})
}
