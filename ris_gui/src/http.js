import axios from "axios";
import { ElLoading, ElMessageBox } from 'element-plus'

let loading

const startLoading = () => {
    loading = ElLoading.service({ fullscreen: true, text: 'Loading' })
}

const endLoading = () => {
    loading.close()
}



axios.interceptors.request.use(config => {
    startLoading()
    let jwt = localStorage.getItem('Token')
    config.headers.Authorization = `Bearer ${jwt}`
    return config
})

axios.interceptors.response.use(response => {
    endLoading()
    let jwt = response.headers['Token']
    if (jwt) {
        localStorage.setItem('Token', jwt)
    }
    return response
}, error => {
    endLoading();
    if (error.response.status === 401) {

        ElMessageBox.alert('Your JSON Web Token (JWT) is expired, please login again.', 'Authorization Error', {
            showClose: false,
            confirmButtonText: "Login",
            callback: () => {
                localStorage.clear()
                sessionStorage.clear()
                location.reload()
            }
        })

    }
    return Promise.reject(error)
})

export default axios

// export const APIurl = 'https://www.fastmock.site/mock/621c7b950c9ece8cc619775913e4d7ee/test'
export const APIurl = 'http://localhost:5000'
export const Testurl = 'https://test-c6c78-default-rtdb.firebaseio.com/'

