let api_url = ""

if (import.meta.env.MODE === 'development') {
    api_url = 'http://localhost:5005' // 本地开发
} else {
    api_url = 'http://100.64.0.2:5005' // 生产环境部署时使用的地址
}

export default api_url