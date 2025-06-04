import React, { useState, useEffect } from 'react';
import { Book, Sparkles, Volume2, ChevronLeft, ChevronRight, Home, User, LogOut, Upload, Wand2, BookOpen, Moon, Sun, Star, Heart } from 'lucide-react';

// Mock authentication context
const AuthContext = React.createContext();

// Auth Provider Component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  
  const login = (username) => {
    const userData = { username, id: Date.now() };
    setUser(userData);
    // Using in-memory storage instead of localStorage
  };
  
  const loginAsGuest = () => {
    setUser({ username: 'Guest', id: 'guest-' + Date.now() });
  };
  
  const logout = () => {
    setUser(null);
  };
  
  return (
    <AuthContext.Provider value={{ user, login, loginAsGuest, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Login Component
const Login = () => {
  const [username, setUsername] = useState('');
  const { login, loginAsGuest } = React.useContext(AuthContext);
  const [isAnimating, setIsAnimating] = useState(false);
  
  const handleLogin = () => {
    if (username.trim()) {
      setIsAnimating(true);
      setTimeout(() => login(username), 500);
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
              setTimeout(loginAsGuest, 500);
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

// Story Generator Component
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
    
    // Create a demo story - "Luna the Bunny's Rainbow Garden"
    const demoStory = {
      id: Date.now(),
      title: "Luna the Bunny's Rainbow Garden",
      pages: [
        { pageNumber: 1, text: "Once upon a time, in a cozy burrow at the edge of a meadow, lived a little white bunny named Luna. She had the softest fur and the biggest, brightest eyes.", illustration: "https://picsum.photos/seed/luna1/800/600" },
        { pageNumber: 2, text: "Luna loved to hop around her garden, but she noticed something sad. All the flowers were the same color - just green leaves everywhere!", illustration: "https://picsum.photos/seed/luna2/800/600" },
        { pageNumber: 3, text: "\"I wish my garden could be as colorful as the rainbow,\" Luna sighed, wiggling her pink nose. That night, she made a special wish upon a twinkling star.", illustration: "https://picsum.photos/seed/luna3/800/600" },
        { pageNumber: 4, text: "The next morning, Luna found a magical seed packet on her doorstep! It sparkled with all the colors of the rainbow and had a note: \"Plant with love.\"", illustration: "https://picsum.photos/seed/luna4/800/600" },
        { pageNumber: 5, text: "Luna carefully planted the seeds in seven neat rows. She watered them with her little blue watering can and sang them a happy song.", illustration: "https://picsum.photos/seed/luna5/800/600" },
        { pageNumber: 6, text: "On the first day, tiny red shoots popped up! \"How wonderful!\" Luna exclaimed, clapping her little paws together with joy.", illustration: "https://picsum.photos/seed/luna6/800/600" },
        { pageNumber: 7, text: "On the second day, orange buds appeared next to the red ones. Luna danced around them, her fluffy tail bouncing with each hop.", illustration: "https://picsum.photos/seed/luna7/800/600" },
        { pageNumber: 8, text: "By the third day, sunny yellow flowers bloomed! They smelled like honey and sunshine. Luna invited her friend Bella the Butterfly to see.", illustration: "https://picsum.photos/seed/luna8/800/600" },
        { pageNumber: 9, text: "\"Your garden is becoming magical!\" said Bella, fluttering her colorful wings. On the fourth day, green leaves unfurled like tiny umbrellas.", illustration: "https://picsum.photos/seed/luna9/800/600" },
        { pageNumber: 10, text: "The fifth day brought beautiful blue blossoms that looked like the sky. Luna's friend Oliver the Owl hooted with delight when he saw them.", illustration: "https://picsum.photos/seed/luna10/800/600" },
        { pageNumber: 11, text: "On the sixth day, purple petals opened wide. They sparkled in the sunlight like tiny amethysts. More friends came to admire Luna's garden.", illustration: "https://picsum.photos/seed/luna11/800/600" },
        { pageNumber: 12, text: "Finally, on the seventh day, violet flowers completed the rainbow! Luna's garden was now the most colorful place in the whole meadow.", illustration: "https://picsum.photos/seed/luna12/800/600" },
        { pageNumber: 13, text: "News of the rainbow garden spread quickly. Soon, animals from all around came to visit. There was Freddy the Fox, Rosie the Robin, and Sam the Squirrel.", illustration: "https://picsum.photos/seed/luna13/800/600" },
        { pageNumber: 14, text: "\"Welcome to my rainbow garden!\" Luna said proudly. \"There's enough beauty for everyone to enjoy!\" The animals gasped at the colorful sight.", illustration: "https://picsum.photos/seed/luna14/800/600" },
        { pageNumber: 15, text: "Luna decided to have a garden party. She set up tiny tables with acorn cups and clover sandwiches. Everyone was invited!", illustration: "https://picsum.photos/seed/luna15/800/600" },
        { pageNumber: 16, text: "Bella the Butterfly brought dewdrop lemonade. Oliver the Owl shared his moonberry muffins. It was the best party ever!", illustration: "https://picsum.photos/seed/luna16/800/600" },
        { pageNumber: 17, text: "As they ate, Luna noticed something special. Each friend matched a color in her garden! Freddy's fur was orange like the marigolds.", illustration: "https://picsum.photos/seed/luna17/800/600" },
        { pageNumber: 18, text: "Rosie's red breast matched the roses. Sam's brown fur looked lovely next to the tree trunks. \"We're all part of the rainbow!\" Luna realized.", illustration: "https://picsum.photos/seed/luna18/800/600" },
        { pageNumber: 19, text: "The friends decided to help Luna care for the garden. They took turns watering, weeding, and singing to the flowers.", illustration: "https://picsum.photos/seed/luna19/800/600" },
        { pageNumber: 20, text: "Every morning, Luna would hop through her garden paths. She loved how the dewdrops on the petals looked like tiny diamonds.", illustration: "https://picsum.photos/seed/luna20/800/600" },
        { pageNumber: 21, text: "One day, a sad little mouse named Milly came by. \"I'm too small and gray,\" she squeaked. \"I don't fit in anywhere.\"", illustration: "https://picsum.photos/seed/luna21/800/600" },
        { pageNumber: 22, text: "Luna hugged Milly gently. \"Every color is special, even gray! You're like the soft morning mist that makes the rainbow appear!\"", illustration: "https://picsum.photos/seed/luna22/800/600" },
        { pageNumber: 23, text: "Luna showed Milly the silver moonflowers that only bloomed at night. \"See? You're magical too!\" Milly's eyes sparkled with happiness.", illustration: "https://picsum.photos/seed/luna23/800/600" },
        { pageNumber: 24, text: "From that day on, Milly helped tend the night garden. She discovered that being different made her special, not strange.", illustration: "https://picsum.photos/seed/luna24/800/600" },
        { pageNumber: 25, text: "As the seasons changed, so did the garden. But the rainbow colors always remained, reminding everyone of the magic of diversity.", illustration: "https://picsum.photos/seed/luna25/800/600" },
        { pageNumber: 26, text: "Luna learned to save seeds from each color. She shared them with other animals who wanted to start their own rainbow gardens.", illustration: "https://picsum.photos/seed/luna26/800/600" },
        { pageNumber: 27, text: "Soon, the whole meadow was dotted with colorful gardens. Each one was unique, just like the animal who tended it.", illustration: "https://picsum.photos/seed/luna27/800/600" },
        { pageNumber: 28, text: "On quiet evenings, Luna would sit in her garden and remember her wish upon the star. She felt grateful for the magic it brought.", illustration: "https://picsum.photos/seed/luna28/800/600" },
        { pageNumber: 29, text: "\"The real magic,\" Luna thought, \"wasn't just the colorful flowers. It was bringing friends together and celebrating our differences.\"", illustration: "https://picsum.photos/seed/luna29/800/600" },
        { pageNumber: 30, text: "And so Luna's rainbow garden grew more beautiful each day, filled with laughter, friendship, and love. The end. 🌈", illustration: "https://picsum.photos/seed/luna30/800/600" }
      ],
      createdAt: new Date().toISOString()
    };
    
    // Simulate API call
    setTimeout(() => {
      if (instructions || uploadedImage) {
        // If custom instructions provided, create a custom story
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
        // Use the demo story
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
              className={`w-full py-4 px-6 rounded-2xl font-bold text-xl text-white transform transition-all duration-200 ${
                isGenerating
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

// Story Viewer Component
const StoryViewer = ({ story, onClose }) => {
  const [currentSpread, setCurrentSpread] = useState(0); // Track page spread (0 = cover + page 1, 1 = pages 2-3, etc.)
  const [isReading, setIsReading] = useState(false);
  const [isFlipping, setIsFlipping] = useState(false);
  
  // Add cover page to the beginning
  const allPages = [
    { pageNumber: 0, text: "", illustration: "cover", isCover: true },
    ...story.pages
  ];
  
  // Calculate left and right page indices
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
  
  // Calculate current visible page numbers
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
                      // Cover page with full-bleed design
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
                      // Story page with full-bleed illustration and overlaid text
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
                      // Empty right side of cover
                      <div className="h-full bg-gradient-to-br from-yellow-200 via-pink-200 to-purple-200 flex items-center justify-center">
                        <p className="text-gray-600 text-lg italic">Turn the page to begin...</p>
                      </div>
                    ) : (
                      // Story page with full-bleed illustration and overlaid text
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
          className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-all transform ${
            currentSpread === 0
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
            className={`p-3 rounded-full transition-all transform ${
              isReading
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
          className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-all transform ${
            rightPageIndex >= allPages.length - 1
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

// Story Library Component
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

// Main App Component
const App = () => {
  const { user, logout } = React.useContext(AuthContext);
  const [activeView, setActiveView] = useState('generator');
  const [stories, setStories] = useState([]);
  const [selectedStory, setSelectedStory] = useState(null);
  
  // Initialize with demo story
  useEffect(() => {
    const demoStory = {
      id: 'demo-story',
      title: "Luna the Bunny's Rainbow Garden",
      pages: [
        { pageNumber: 1, text: "Once upon a time, in a cozy burrow at the edge of a meadow, lived a little white bunny named Luna. She had the softest fur and the biggest, brightest eyes.", illustration: "https://picsum.photos/seed/luna1/800/600" },
        { pageNumber: 2, text: "Luna loved to hop around her garden, but she noticed something sad. All the flowers were the same color - just green leaves everywhere!", illustration: "https://picsum.photos/seed/luna2/800/600" },
        { pageNumber: 3, text: "\"I wish my garden could be as colorful as the rainbow,\" Luna sighed, wiggling her pink nose. That night, she made a special wish upon a twinkling star.", illustration: "https://picsum.photos/seed/luna3/800/600" },
        { pageNumber: 4, text: "The next morning, Luna found a magical seed packet on her doorstep! It sparkled with all the colors of the rainbow and had a note: \"Plant with love.\"", illustration: "https://picsum.photos/seed/luna4/800/600" },
        { pageNumber: 5, text: "Luna carefully planted the seeds in seven neat rows. She watered them with her little blue watering can and sang them a happy song.", illustration: "https://picsum.photos/seed/luna5/800/600" },
        { pageNumber: 6, text: "On the first day, tiny red shoots popped up! \"How wonderful!\" Luna exclaimed, clapping her little paws together with joy.", illustration: "https://picsum.photos/seed/luna6/800/600" },
        { pageNumber: 7, text: "On the second day, orange buds appeared next to the red ones. Luna danced around them, her fluffy tail bouncing with each hop.", illustration: "https://picsum.photos/seed/luna7/800/600" },
        { pageNumber: 8, text: "By the third day, sunny yellow flowers bloomed! They smelled like honey and sunshine. Luna invited her friend Bella the Butterfly to see.", illustration: "https://picsum.photos/seed/luna8/800/600" },
        { pageNumber: 9, text: "\"Your garden is becoming magical!\" said Bella, fluttering her colorful wings. On the fourth day, green leaves unfurled like tiny umbrellas.", illustration: "https://picsum.photos/seed/luna9/800/600" },
        { pageNumber: 10, text: "The fifth day brought beautiful blue blossoms that looked like the sky. Luna's friend Oliver the Owl hooted with delight when he saw them.", illustration: "https://picsum.photos/seed/luna10/800/600" },
        { pageNumber: 11, text: "On the sixth day, purple petals opened wide. They sparkled in the sunlight like tiny amethysts. More friends came to admire Luna's garden.", illustration: "https://picsum.photos/seed/luna11/800/600" },
        { pageNumber: 12, text: "Finally, on the seventh day, violet flowers completed the rainbow! Luna's garden was now the most colorful place in the whole meadow.", illustration: "https://picsum.photos/seed/luna12/800/600" },
        { pageNumber: 13, text: "News of the rainbow garden spread quickly. Soon, animals from all around came to visit. There was Freddy the Fox, Rosie the Robin, and Sam the Squirrel.", illustration: "https://picsum.photos/seed/luna13/800/600" },
        { pageNumber: 14, text: "\"Welcome to my rainbow garden!\" Luna said proudly. \"There's enough beauty for everyone to enjoy!\" The animals gasped at the colorful sight.", illustration: "https://picsum.photos/seed/luna14/800/600" },
        { pageNumber: 15, text: "Luna decided to have a garden party. She set up tiny tables with acorn cups and clover sandwiches. Everyone was invited!", illustration: "https://picsum.photos/seed/luna15/800/600" },
        { pageNumber: 16, text: "Bella the Butterfly brought dewdrop lemonade. Oliver the Owl shared his moonberry muffins. It was the best party ever!", illustration: "https://picsum.photos/seed/luna16/800/600" },
        { pageNumber: 17, text: "As they ate, Luna noticed something special. Each friend matched a color in her garden! Freddy's fur was orange like the marigolds.", illustration: "https://picsum.photos/seed/luna17/800/600" },
        { pageNumber: 18, text: "Rosie's red breast matched the roses. Sam's brown fur looked lovely next to the tree trunks. \"We're all part of the rainbow!\" Luna realized.", illustration: "https://picsum.photos/seed/luna18/800/600" },
        { pageNumber: 19, text: "The friends decided to help Luna care for the garden. They took turns watering, weeding, and singing to the flowers.", illustration: "https://picsum.photos/seed/luna19/800/600" },
        { pageNumber: 20, text: "Every morning, Luna would hop through her garden paths. She loved how the dewdrops on the petals looked like tiny diamonds.", illustration: "https://picsum.photos/seed/luna20/800/600" },
        { pageNumber: 21, text: "One day, a sad little mouse named Milly came by. \"I'm too small and gray,\" she squeaked. \"I don't fit in anywhere.\"", illustration: "https://picsum.photos/seed/luna21/800/600" },
        { pageNumber: 22, text: "Luna hugged Milly gently. \"Every color is special, even gray! You're like the soft morning mist that makes the rainbow appear!\"", illustration: "https://picsum.photos/seed/luna22/800/600" },
        { pageNumber: 23, text: "Luna showed Milly the silver moonflowers that only bloomed at night. \"See? You're magical too!\" Milly's eyes sparkled with happiness.", illustration: "https://picsum.photos/seed/luna23/800/600" },
        { pageNumber: 24, text: "From that day on, Milly helped tend the night garden. She discovered that being different made her special, not strange.", illustration: "https://picsum.photos/seed/luna24/800/600" },
        { pageNumber: 25, text: "As the seasons changed, so did the garden. But the rainbow colors always remained, reminding everyone of the magic of diversity.", illustration: "https://picsum.photos/seed/luna25/800/600" },
        { pageNumber: 26, text: "Luna learned to save seeds from each color. She shared them with other animals who wanted to start their own rainbow gardens.", illustration: "https://picsum.photos/seed/luna26/800/600" },
        { pageNumber: 27, text: "Soon, the whole meadow was dotted with colorful gardens. Each one was unique, just like the animal who tended it.", illustration: "https://picsum.photos/seed/luna27/800/600" },
        { pageNumber: 28, text: "On quiet evenings, Luna would sit in her garden and remember her wish upon the star. She felt grateful for the magic it brought.", illustration: "https://picsum.photos/seed/luna28/800/600" },
        { pageNumber: 29, text: "\"The real magic,\" Luna thought, \"wasn't just the colorful flowers. It was bringing friends together and celebrating our differences.\"", illustration: "https://picsum.photos/seed/luna29/800/600" },
        { pageNumber: 30, text: "And so Luna's rainbow garden grew more beautiful each day, filled with laughter, friendship, and love. The end. 🌈", illustration: "https://picsum.photos/seed/luna30/800/600" }
      ],
      createdAt: new Date().toISOString()
    };
    setStories([demoStory]);
  }, []);
  
  const handleStoryGenerated = (story) => {
    const newStories = [story, ...stories];
    setStories(newStories);
    setSelectedStory(story);
  };
  
  if (!user) {
    return <Login />;
  }
  
  if (selectedStory) {
    return (
      <StoryViewer
        story={selectedStory}
        onClose={() => setSelectedStory(null)}
      />
    );
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-200 via-pink-200 to-purple-200">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-full p-3">
              <Book className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-800">Magic Storybook</h1>
          </div>
          
          <nav className="flex items-center space-x-4">
            <button
              onClick={() => setActiveView('generator')}
              className={`px-4 py-2 rounded-full font-semibold transition-all ${
                activeView === 'generator'
                  ? 'bg-purple-500 text-white'
                  : 'text-gray-600 hover:bg-purple-100'
              }`}
            >
              Create Story
            </button>
            <button
              onClick={() => setActiveView('library')}
              className={`px-4 py-2 rounded-full font-semibold transition-all ${
                activeView === 'library'
                  ? 'bg-purple-500 text-white'
                  : 'text-gray-600 hover:bg-purple-100'
              }`}
            >
              My Stories
            </button>
            
            <div className="flex items-center space-x-2 ml-4">
              <User className="w-5 h-5 text-gray-600" />
              <span className="text-gray-700 font-medium">{user.username}</span>
              <button
                onClick={logout}
                className="text-red-500 hover:text-red-700 ml-2"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </nav>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="p-4">
        {activeView === 'generator' ? (
          <StoryGenerator onStoryGenerated={handleStoryGenerated} />
        ) : (
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
              Your Story Collection
            </h2>
            {stories.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="w-20 h-20 text-gray-400 mx-auto mb-4" />
                <p className="text-xl text-gray-600">
                  No stories yet! Create your first magical story!
                </p>
              </div>
            ) : (
              <StoryLibrary
                stories={stories}
                onSelectStory={setSelectedStory}
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
};

// Root Component
export default function StoryBookApp() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}