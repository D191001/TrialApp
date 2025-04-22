import api from './config'

export const checkBackendHealth = async () => {
    try {
        const response = await api.get('/health-check')
        return response.data.status === 'healthy'
    } catch (error) {
        console.error('Backend health check failed:', error)
        return false
    }
}
