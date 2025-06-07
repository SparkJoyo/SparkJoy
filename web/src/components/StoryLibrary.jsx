import React from 'react';
import { BookOpen } from 'lucide-react';

const StoryLibrary = ({ stories, onSelectStory }) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {stories.map((story) => (
                <div
                    key={story.id}
                    onClick={() => onSelectStory(story)}
                    className="bg-white rounded-2xl shadow-lg overflow-hidden cursor-pointer transform hover:scale-105 transition-all duration-200"
                >
                    <div className="h-48 bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center">
                        <BookOpen className="w-20 h-20 text-white" />
                    </div>
                    <div className="p-4">
                        <h3 className="text-xl font-bold text-gray-800 mb-2">{story.title}</h3>
                        <p className="text-gray-600 text-sm">
                            Created on {new Date(story.createdAt).toLocaleDateString()}
                        </p>
                        <p className="text-purple-600 font-semibold mt-2">
                            {story.pages.length} pages
                        </p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default StoryLibrary;