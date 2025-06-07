import React, { useState, useEffect } from 'react';
import { Sparkles, ChevronLeft, ChevronRight, Home, Volume2 } from 'lucide-react';

const StoryViewer = ({ story, onClose }) => {
    const [currentSpread, setCurrentSpread] = useState(0);
    const [isReading, setIsReading] = useState(false);
    const [isFlipping, setIsFlipping] = useState(false);

    const allPages = [
        { pageNumber: 0, text: "", illustration: "cover", isCover: true },
        ...story.pages
    ];

    const leftPageIndex = currentSpread * 2;
    const rightPageIndex = currentSpread * 2 + 1;
    const leftPage = allPages[leftPageIndex];
    const rightPage = allPages[rightPageIndex];

    const nextSpread = () => {
        if (rightPageIndex < allPages.length - 1) {
            setIsFlipping(true);
            setTimeout(() => {
                setCurrentSpread(currentSpread + 1);
                setIsFlipping(false);
            }, 300);
        }
    };

    const prevSpread = () => {
        if (currentSpread > 0) {
            setIsFlipping(true);
            setTimeout(() => {
                setCurrentSpread(currentSpread - 1);
                setIsFlipping(false);
            }, 300);
        }
    };

    const readAloud = () => {
        if ('speechSynthesis' in window) {
            if (isReading) {
                window.speechSynthesis.cancel();
                setIsReading(false);
            } else {
                let textToRead = '';
                if (leftPage && !leftPage.isCover) textToRead += leftPage.text + ' ';
                if (rightPage && !rightPage.isCover) textToRead += rightPage.text;
                if (textToRead) {
                    const utterance = new SpeechSynthesisUtterance(textToRead);
                    utterance.rate = 0.8;
                    utterance.pitch = 1.2;
                    utterance.onend = () => setIsReading(false);
                    window.speechSynthesis.speak(utterance);
                    setIsReading(true);
                }
            }
        }
    };

    useEffect(() => {
        return () => {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
        };
    }, []);

    const getPageNumbers = () => {
        const visiblePages = [];
        if (leftPage && !leftPage.isCover) visiblePages.push(leftPage.pageNumber);
        if (rightPage && !rightPage.isCover) visiblePages.push(rightPage.pageNumber);
        return visiblePages;
    };

    const pageNumbers = getPageNumbers();
    const pageDisplay = pageNumbers.length > 0 ?
        (pageNumbers.length === 1 ? `Page ${pageNumbers[0]}` : `Page ${pageNumbers[0]}/${pageNumbers[1]}`) :
        'Cover';

    return (
        <div className="fixed inset-0 bg-gray-100 z-50 overflow-hidden">
            {/* Header bar */}
            <div className="absolute top-0 left-0 right-0 bg-gradient-to-r from-pink-500 to-purple-500 h-16 flex items-center justify-between px-6 shadow-lg z-20">
                <div className="text-white font-bold text-lg">
                    {story.title}
                </div>
                <div className="text-white font-medium">
                    {pageDisplay}
                </div>
                <button
                    onClick={onClose}
                    className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full p-2 transition-all"
                >
                    <Home className="w-5 h-5 text-white" />
                </button>
            </div>
            {/* Book container */}
            <div className="h-full pt-16 pb-20 flex items-center justify-center px-4">
                <div className="relative max-w-7xl w-full h-full">
                    <div className={`relative h-full transition-transform duration-300 ${isFlipping ? 'scale-98' : 'scale-100'}`}>
                        {/* Book spine/binding */}
                        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-1 h-full bg-gray-300 shadow-inner z-10"></div>
                        {/* Double page spread */}
                        <div className="relative h-full flex shadow-2xl rounded-lg overflow-hidden">
                            {/* Left page */}
                            <div className="relative w-1/2 h-full bg-white overflow-hidden">
                                {leftPage && (
                                    <>
                                        {leftPage.isCover ? (
                                            <div className="relative h-full bg-gradient-to-br from-purple-400 via-pink-400 to-yellow-400">
                                                <div className="absolute inset-0 flex items-center justify-center">
                                                    <div className="text-center p-8">
                                                        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 drop-shadow-lg">
                                                            {story.title}
                                                        </h1>
                                                        <div className="w-48 h-48 md:w-64 md:h-64 mx-auto bg-white bg-opacity-90 rounded-full flex items-center justify-center shadow-2xl">
                                                            <Sparkles className="w-24 h-24 md:w-32 md:h-32 text-purple-500" />
                                                        </div>
                                                        <p className="mt-8 text-xl md:text-2xl text-white font-medium drop-shadow">
                                                            A Magical Story
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="relative h-full">
                                                <img
                                                    src={leftPage.illustration}
                                                    alt={`Page ${leftPage.pageNumber}`}
                                                    className="absolute inset-0 w-full h-full object-cover"
                                                />
                                                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black to-transparent bg-opacity-60 p-6 md:p-10">
                                                    <p className="text-white text-xl md:text-2xl lg:text-3xl leading-relaxed font-medium drop-shadow-lg">
                                                        {leftPage.text}
                                                    </p>
                                                </div>
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                            {/* Right page */}
                            <div className="relative w-1/2 h-full bg-white overflow-hidden">
                                {rightPage && (
                                    <>
                                        {rightPage.isCover ? (
                                            <div className="h-full bg-gradient-to-br from-yellow-200 via-pink-200 to-purple-200 flex items-center justify-center">
                                                <p className="text-gray-600 text-lg italic">Turn the page to begin...</p>
                                            </div>
                                        ) : (
                                            <div className="relative h-full">
                                                <img
                                                    src={rightPage.illustration}
                                                    alt={`Page ${rightPage.pageNumber}`}
                                                    className="absolute inset-0 w-full h-full object-cover"
                                                />
                                                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black to-transparent bg-opacity-60 p-6 md:p-10">
                                                    <p className="text-white text-xl md:text-2xl lg:text-3xl leading-relaxed font-medium drop-shadow-lg">
                                                        {rightPage.text}
                                                    </p>
                                                </div>
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {/* Bottom navigation bar */}
            <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200 h-20 flex items-center justify-between px-6 shadow-lg">
                <button
                    onClick={prevSpread}
                    disabled={currentSpread === 0}
                    className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-all transform ${currentSpread === 0
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg hover:scale-105'
                        }`}
                >
                    <ChevronLeft className="w-6 h-6" />
                    <span className="font-medium">Previous</span>
                </button>
                <div className="flex items-center space-x-4">
                    <button
                        onClick={readAloud}
                        className={`p-3 rounded-full transition-all transform ${isReading
                            ? 'bg-gradient-to-r from-pink-500 to-red-500 animate-pulse shadow-lg'
                            : 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:shadow-lg hover:scale-105'
                            } text-white`}
                    >
                        <Volume2 className="w-6 h-6" />
                    </button>
                    <div className="text-gray-600 font-medium">
                        {pageDisplay} of {story.pages.length}
                    </div>
                </div>
                <button
                    onClick={nextSpread}
                    disabled={rightPageIndex >= allPages.length - 1}
                    className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-all transform ${rightPageIndex >= allPages.length - 1
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg hover:scale-105'
                        }`}
                >
                    <span className="font-medium">Next</span>
                    <ChevronRight className="w-6 h-6" />
                </button>
            </div>
        </div>
    );
};

export default StoryViewer;