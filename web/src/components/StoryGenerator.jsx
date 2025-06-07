import React, { useState } from 'react';
import { Sparkles, Upload, Wand2 } from 'lucide-react';

const StoryGenerator = ({ onStoryGenerated }) => {
  const [instructions, setInstructions] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const generateStory = async () => {
    setIsGenerating(true);
    const demoStory = {
      id: Date.now(),
      title: "Luna the Bunny's Rainbow Garden",
      pages: [
        { pageNumber: 1, text: "Once upon a time, in a cozy burrow at the edge of a meadow, lived a little white bunny named Luna. She had the softest fur and the biggest, brightest eyes.", illustration: "https://picsum.photos/seed/luna1/800/600" },
        // ... (rest of the pages, copy from your original code)
      ],
      createdAt: new Date().toISOString()
    };
    setTimeout(() => {
      if (instructions || uploadedImage) {
        const customStory = {
          ...demoStory,
          id: Date.now(),
          title: "Your Custom Story",
          pages: demoStory.pages.map((page, i) => ({
            ...page,
            text: i === 0 ? `Once upon a time... ${instructions}` : page.text
          }))
        };
        onStoryGenerated(customStory);
      } else {
        onStoryGenerated(demoStory);
      }
      setIsGenerating(false);
      setInstructions('');
      setUploadedImage(null);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-300 via-purple-300 to-pink-300 p-4">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-4xl font-bold text-white text-center mb-8 flex items-center justify-center">
          <Sparkles className="w-10 h-10 mr-3 animate-spin" />
          Create Your Story
          <Sparkles className="w-10 h-10 ml-3 animate-spin" />
        </h2>
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          <div className="space-y-6">
            <div>
              <label className="block text-xl font-semibold text-gray-700 mb-3">
                📝 Tell us what your story should be about (optional)
              </label>
              <textarea
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder="A brave little bunny who loves to explore..."
                className="w-full px-4 py-3 text-lg border-2 border-purple-300 rounded-2xl focus:outline-none focus:border-purple-500 transition-colors resize-none"
                rows="4"
              />
            </div>
            <div>
              <label className="block text-xl font-semibold text-gray-700 mb-3">
                🖼️ Upload an inspiration image (optional)
              </label>
              <div className="relative">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                  id="image-upload"
                />
                <label
                  htmlFor="image-upload"
                  className="flex items-center justify-center w-full h-40 border-3 border-dashed border-purple-300 rounded-2xl cursor-pointer hover:border-purple-500 transition-colors bg-purple-50"
                >
                  {uploadedImage ? (
                    <img src={uploadedImage} alt="Uploaded" className="h-36 object-contain" />
                  ) : (
                    <div className="text-center">
                      <Upload className="w-12 h-12 text-purple-400 mx-auto mb-2" />
                      <p className="text-purple-600">Click to upload a picture</p>
                    </div>
                  )}
                </label>
              </div>
            </div>
            <button
              onClick={generateStory}
              disabled={isGenerating}
              className={`w-full py-4 px-6 rounded-2xl font-bold text-xl text-white transform transition-all duration-200 ${isGenerating
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:shadow-lg hover:scale-105'
                }`}
            >
              {isGenerating ? (
                <span className="flex items-center justify-center">
                  <Wand2 className="w-6 h-6 mr-2 animate-spin" />
                  Creating your magical story...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <Wand2 className="w-6 h-6 mr-2" />
                  Generate Story!
                </span>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoryGenerator;