import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Book, Star, Heart, Moon } from 'lucide-react';
import { AuthContext } from './AuthProvider';

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const { login, loginAsGuest } = useContext(AuthContext);
    const [isAnimating, setIsAnimating] = useState(false);

    const handleLogin = () => {
        if (username.trim()) {
            setIsAnimating(true);
            setTimeout(() => {
                login(username);
                navigate('/create');
            }, 500);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleLogin();
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-300 to-yellow-300 flex items-center justify-center p-4">
            <div className={`bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full transform transition-all duration-500 ${isAnimating ? 'scale-0 rotate-180' : 'scale-100'}`}>
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mb-4 animate-bounce">
                        <Book className="w-10 h-10 text-white" />
                    </div>
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Magic Storybook</h1>
                    <p className="text-gray-600">Enter your name to start creating stories!</p>
                </div>
                <div className="space-y-4">
                    <div>
                        <input
                            type="text"
                            placeholder="What's your name?"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            onKeyPress={handleKeyPress}
                            className="w-full px-4 py-3 text-lg border-2 border-purple-300 rounded-2xl focus:outline-none focus:border-purple-500 transition-colors"
                        />
                    </div>
                    <button
                        onClick={handleLogin}
                        className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 px-6 rounded-2xl hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                    >
                        Start Creating! ✨
                    </button>
                </div>
                <div className="mt-4">
                    <button
                        onClick={() => {
                            setIsAnimating(true);
                            setTimeout(() => {
                                loginAsGuest();
                                navigate('/create');
                            }, 500);
                        }}
                        className="w-full bg-gradient-to-r from-yellow-400 to-orange-400 text-white font-bold py-3 px-6 rounded-2xl hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                    >
                        Continue as Guest 🌟
                    </button>
                </div>
                <div className="mt-6 flex justify-center space-x-2">
                    <Star className="w-6 h-6 text-yellow-400 animate-pulse" />
                    <Heart className="w-6 h-6 text-pink-400 animate-pulse delay-100" />
                    <Moon className="w-6 h-6 text-purple-400 animate-pulse delay-200" />
                </div>
            </div>
        </div>
    );
};

export default Login;