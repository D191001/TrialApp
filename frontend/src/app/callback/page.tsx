'use client';

import { Suspense } from 'react';
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import axios from 'axios';
import { toast } from 'react-hot-toast';

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const handleCallback = async () => {
            const code = searchParams.get('code');

            if (!code) {
                toast.error('Код авторизации не получен');
                router.push('/');
                return;
            }

            try {
                const response = await axios.get(`/api/v1/auth/yandex/callback?code=${code}`);
                const { access_token } = response.data;

                if (access_token) {
                    localStorage.setItem('token', access_token);
                    toast.success('Авторизация успешна!');
                    router.push('/');
                }
            } catch (error: any) {
                console.error('Callback error:', error);
                toast.error(error.response?.data?.detail || 'Ошибка при авторизации через Яндекс');
                router.push('/');
            }
        };

        handleCallback();
    }, [router, searchParams]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Выполняется вход...</p>
            </div>
        </div>
    );
}

export default function YandexCallback() {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Загрузка...</p>
                </div>
            </div>
        }>
            <CallbackContent />
        </Suspense>
    );
}