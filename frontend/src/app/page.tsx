'use client';

import { useState, useEffect } from 'react';
import AuthButton from '@/components/AuthButton';
import AuthForm from '@/components/AuthForm';
import { toast } from 'react-hot-toast';
import axios from 'axios';

interface User {
    id: string;
    email: string;
    name: string;
    avatar?: string;
}

export default function Home() {
    const [showAuth, setShowAuth] = useState(false);
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            fetchUserData(token);
        }
    }, []);

    const fetchUserData = async (token: string) => {
        try {
            // Используем endpoint /api/v1/profile для получения данных пользователя
            const response = await axios.get('/api/v1/profile', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(response.data);
        } catch (error) {
            console.error('Error fetching user data:', error);
            localStorage.removeItem('token');
            setUser(null);
            toast.error('Ошибка при получении данных пользователя');
        }
    };

    const handleAuth = async (email: string, password: string, isRegister: boolean) => {
        try {
            const endpoint = isRegister ? '/api/v1/auth/register' : '/api/v1/auth/login';
            const response = await axios.post(endpoint, {
                email,
                password,
                name: email.split('@')[0] // Используем часть email как имя при регистрации
            });

            const { access_token } = response.data;
            localStorage.setItem('token', access_token);
            await fetchUserData(access_token);
            setShowAuth(false);
            toast.success(isRegister ? 'Регистрация успешна!' : 'Вход выполнен успешно!');
        } catch (error: any) {
            console.error('Auth error:', error);
            toast.error(error.response?.data?.detail || 'Ошибка авторизации');
        }
    };

    const handleYandexAuth = async () => {
        try {
            const response = await axios.get('/api/v1/auth/yandex');
            window.location.href = response.data.auth_url;
        } catch (error) {
            console.error('Yandex auth error:', error);
            toast.error('Ошибка при авторизации через Яндекс');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        toast.success('Вы успешно вышли из системы');
    };

    if (!showAuth && !user) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <AuthButton onClick={() => setShowAuth(true)}>
                    Войти или зарегистрироваться
                </AuthButton>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-4xl mx-auto p-6">
                {showAuth && !user ? (
                    <AuthForm onSubmit={handleAuth} onYandexAuth={handleYandexAuth} />
                ) : user ? (
                    <div className="bg-white shadow-lg rounded-lg p-6">
                        <div className="flex justify-between items-center mb-6">
                            <div>
                                <h2 className="text-2xl font-bold">Добро пожаловать!</h2>
                                <p className="text-gray-600">{user.email}</p>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition duration-200"
                            >
                                Выйти
                            </button>
                        </div>
                        {user.avatar && (
                            <img
                                src={user.avatar}
                                alt="Аватар пользователя"
                                className="w-20 h-20 rounded-full mb-4"
                            />
                        )}
                    </div>
                ) : null}
            </div>
        </div>
    );
}