'use client';

import { useState } from 'react';

interface Review {
    id: number;
    text: string;
    email: string;
}

interface ReviewFormProps {
    onSubmit: (text: string) => void;
    reviews: Review[];
}

export default function ReviewForm({ onSubmit, reviews }: ReviewFormProps) {
    const [text, setText] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(text);
        setText('');
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="text" className="block text-sm font-medium text-gray-700">
                        Ваш отзыв
                    </label>
                    <textarea
                        id="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        rows={4}
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        required
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Отправить отзыв
                </button>
            </form>

            <div className="space-y-4">
                <h2 className="text-2xl font-bold">Отзывы</h2>
                {reviews.length === 0 ? (
                    <p className="text-gray-500">Пока нет отзывов</p>
                ) : (
                    reviews.map((review) => (
                        <div key={review.id} className="border p-4 rounded-lg">
                            <p className="text-sm text-gray-600 mb-2">Автор: {review.email}</p>
                            <p className="text-gray-800">{review.text}</p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}