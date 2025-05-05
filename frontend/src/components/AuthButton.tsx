'use client';

interface AuthButtonProps {
    onClick?: () => void;
    children?: React.ReactNode;
}

export default function AuthButton({ onClick, children }: AuthButtonProps) {
    return (
        <button
            onClick={onClick}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
            {children}
        </button>
    );
}