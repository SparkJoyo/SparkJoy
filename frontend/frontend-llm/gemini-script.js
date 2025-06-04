import React, { useState, useEffect, useRef, useCallback } from 'react';
import { create } from 'zustand';
import { initializeApp } from 'firebase/app';
import {
    getAuth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signInAnonymously,
    onAuthStateChanged,
    signOut,
    setPersistence,
    browserLocalPersistence // Or browserSessionPersistence
} from 'firebase/auth';
import {
    getFirestore,
    collection,
    addDoc,
    doc,
    setDoc,
    getDoc,
    getDocs,
    query,
    where,
    orderBy,
    Timestamp,
    onSnapshot,
    deleteDoc
} from 'firebase/firestore';
import {
    ChevronLeft,
    ChevronRight,
    BookOpen,
    PlusCircle,
    ImageIcon,
    LogOut,
    LogIn,
    UserPlus,
    Volume2,
    Trash2,
    Loader2,
    FileText,
    Sparkles,
    XCircle,
    UploadCloud,
    Info,
    Camera 
} from 'lucide-react';

// --- Firebase Configuration ---
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-storybook-app';

// Initialize Firebase
let app;
let auth;
let db;

try {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    db = getFirestore(app);
    setPersistence(auth, browserLocalPersistence);
} catch (error) {
    console.error("Error initializing Firebase:", error);
}

// --- Demo Story Definition ---
const demoStory = {
    id: 'demo-story-001',
    title: 'Barnaby Bear and the Fallen Star',
    pages: [
        {
            text: "Barnaby was a curious little bear who lived in a sun-dappled forest. He loved honey, naps, and most of all, gazing at the twinkling stars each night.",
            imageUrl: "https://placehold.co/800x600/A0D2DB/333333?text=Barnaby+in+Forest&font=lora",
            pageNum: 1
        },
        {
            text: "One evening, as the sky turned a deep velvet blue, Barnaby saw something amazing! A tiny, shimmering star tumbled down, landing with a soft plink in the nearby Whispering Woods.",
            imageUrl: "https://placehold.co/800x600/E0C3FC/5D3A9A?text=Falling+Star&font=lora",
            pageNum: 2
        },
        {
            text: "With a gulp of courage and a map drawn on a leaf (mostly squiggles), Barnaby set off. 'I must help that little star get back home!' he thought.",
            imageUrl: "https://placehold.co/800x600/FFC0CB/333333?text=Barnaby+with+Map&font=lora",
            pageNum: 3
        },
        {
            text: "He met a wise old owl who told him, 'The tallest tree on Blueberry Hill touches the sky. Perhaps the star can launch from there!'",
            imageUrl: "https://placehold.co/800x600/C1E1C1/3B5323?text=Wise+Owl&font=lora",
            pageNum: 4
        },
        {
            text: "After a long climb, Barnaby and the little star reached the top. With a mighty heave from Barnaby and a joyful twinkle, the star zoomed back into the night sky, winking its thanks. Barnaby felt like the bravest bear in the world.",
            imageUrl: "https://placehold.co/800x600/89CFF0/2A52BE?text=Star+Returns&font=lora",
            pageNum: 5
        }
    ],
    createdAt: Timestamp.fromDate(new Date('2024-01-01T10:00:00Z')), 
    userId: 'guest-demo-user', 
    coverImageUrl: "https://placehold.co/300x200/A0D2DB/333333?text=Barnaby+Cover&font=lora",
    isDemo: true 
};


// --- Zustand Stores ---
const useAuthStore = create((set) => ({
    user: null,
    userId: null,
    isGuest: false,
    isLoading: true,
    error: null,
    setUser: (user) => set({ user, userId: user ? user.uid : null, isLoading: false, isGuest: user ? user.isAnonymous : false, error: null }),
    setLoading: (isLoading) => set({ isLoading }),
    setError: (error) => set({ error, isLoading: false }),
    logout: () => set({ user: null, userId: null, isGuest: false, isLoading: false, error: null }),
}));

const useStoryStore = create((set, get) => ({
    stories: [],
    currentStory: null,
    isLoading: false,
    error: null,
    setStories: (stories) => set({ stories }),
    setCurrentStory: (story) => set({ currentStory: story }),
    addStory: (story) => set((state) => {
        if (state.stories.find(s => s.id === story.id)) {
            return state;
        }
        return { stories: [story, ...state.stories] };
    }),
    updateStory: (updatedStory) => set(state => ({
        stories: state.stories.map(story => story.id === updatedStory.id ? updatedStory : story),
        currentStory: state.currentStory && state.currentStory.id === updatedStory.id ? updatedStory : state.currentStory,
    })),
    deleteStoryState: (storyId) => set(state => ({
        stories: state.stories.filter(story => story.id !== storyId),
        currentStory: state.currentStory && state.currentStory.id === storyId ? null : state.currentStory,
    })),
    setLoading: (isLoading) => set({ isLoading }),
    setError: (error) => set({ error, isLoading: false }),
}));

const useNavStore = create((set) => ({
    currentPage: 'auth', 
    storyIdToView: null,
    navigateTo: (page, storyId = null) => set({ currentPage: page, storyIdToView: storyId }),
}));

const GEMINI_API_KEY = ""; 
const IMAGEN_API_KEY = ""; 

const generateRandomId = () => Math.random().toString(36).substring(2, 15);

const imageFileToBase64 = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve({ name: file.name, type: file.type, base64: reader.result.split(',')[1]}); 
    reader.onerror = error => reject(error);
});

const LoadingSpinner = ({ size = 8 }) => (
    <Loader2 className={`animate-spin h-${size} w-${size} text-pink-500`} />
);

const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md transform transition-all">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold text-pink-600">{title}</h3>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <XCircle size={24} />
                    </button>
                </div>
                <div>{children}</div>
            </div>
        </div>
    );
};

const Navbar = () => {
    const { user, isGuest, logout: authLogout } = useAuthStore();
    const { navigateTo } = useNavStore();
    const storyStoreLogout = useStoryStore(state => state.setStories); 

    const handleLogout = async () => {
        try {
            if (auth && auth.currentUser && !auth.currentUser.isAnonymous) {
                 await signOut(auth);
            }
            authLogout();
            storyStoreLogout([]); 
            navigateTo('auth');
        } catch (error) {
            console.error("Error signing out:", error);
            useAuthStore.getState().setError(error.message);
        }
    };

    return (
        <nav className="bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 p-4 shadow-lg sticky top-0 z-40">
            <div className="container mx-auto flex justify-between items-center">
                <div
                    className="text-white text-2xl font-bold flex items-center cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={() => navigateTo(user ? 'generate' : 'auth')}
                >
                    <Sparkles size={28} className="mr-2" /> StorySpark AI
                </div>
                <div className="space-x-2 sm:space-x-4 flex items-center">
                    {user && (
                        <>
                            <button
                                onClick={() => navigateTo('generate')}
                                className="text-white hover:text-yellow-300 transition-colors flex items-center px-2 py-1 rounded-md"
                                title="Create New Story"
                            >
                                <PlusCircle size={20} className="mr-1 sm:mr-2" /> <span className="hidden sm:inline">Create</span>
                            </button>
                            <button
                                onClick={() => navigateTo('previous')}
                                className="text-white hover:text-yellow-300 transition-colors flex items-center px-2 py-1 rounded-md"
                                title="My Stories"
                            >
                                <BookOpen size={20} className="mr-1 sm:mr-2" /> <span className="hidden sm:inline">My Stories</span>
                            </button>
                            <button
                                onClick={handleLogout}
                                className="text-white hover:text-yellow-300 transition-colors flex items-center px-2 py-1 rounded-md"
                                title={isGuest ? "Exit Guest Mode" : "Logout"}
                            >
                                <LogOut size={20} className="mr-1 sm:mr-2" /> <span className="hidden sm:inline">{isGuest ? "Exit" : "Logout"}</span>
                            </button>
                             {isGuest && <span className="text-xs text-yellow-200 hidden md:inline">(Guest)</span>}
                             {!isGuest && auth.currentUser?.email && <span className="text-xs text-yellow-200 hidden md:inline">({auth.currentUser.email.split('@')[0]})</span>}
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

const AuthPage = () => {
    const { setUser, setLoading, setError, error: authError } = useAuthStore();
    const { navigateTo } = useNavStore();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [modalOpen, setModalOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState('');


    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!auth) {
            setModalMessage("Firebase not initialized. Please try again later.");
            setModalOpen(true);
            return;
        }
        setIsSubmitting(true);
        setLoading(true);
        setError(null);
        try {
            let userCredential;
            if (isLogin) {
                userCredential = await signInWithEmailAndPassword(auth, email, password);
            } else {
                userCredential = await createUserWithEmailAndPassword(auth, email, password);
            }
            setUser(userCredential.user);
            navigateTo('generate');
        } catch (err) {
            console.error("Auth error:", err);
            setError(err.message);
            setModalMessage(err.message);
            setModalOpen(true);
        } finally {
            setIsSubmitting(false);
            setLoading(false);
        }
    };

    const handleGuestLogin = async () => {
        if (!auth) {
            setModalMessage("Firebase not initialized. Please try again later.");
            setModalOpen(true);
            return;
        }
        setIsSubmitting(true);
        setLoading(true);
        setError(null);
        try {
            const userCredential = await signInAnonymously(auth);
            setUser(userCredential.user);
            navigateTo('generate');
        } catch (err) {
            console.error("Guest login error:", err);
            setError(err.message);
            setModalMessage(err.message);
            setModalOpen(true);
        } finally {
            setIsSubmitting(false);
            setLoading(false);
        }
    };
    
    useEffect(() => {
        if (authError) {
            setModalMessage(authError);
            setModalOpen(true);
        }
    }, [authError]);


    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-200 via-pink-200 to-indigo-200 p-4">
            <div className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md transform transition-all hover:shadow-3xl">
                <div className="text-center mb-8">
                    <Sparkles size={48} className="mx-auto text-pink-500 mb-2" />
                    <h1 className="text-3xl font-bold text-gray-700">Welcome to StorySpark AI!</h1>
                    <p className="text-gray-500">Let's create magical stories together.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-pink-500 focus:border-pink-500 transition-shadow"
                            placeholder="you@example.com"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-pink-500 focus:border-pink-500 transition-shadow"
                            placeholder="••••••••"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="w-full bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center"
                    >
                        {isSubmitting ? <LoadingSpinner size={5}/> : (isLogin ? <><LogIn size={18} className="mr-2"/> Login</> : <><UserPlus size={18} className="mr-2"/> Sign Up</>)}
                    </button>
                </form>

                <div className="mt-6 text-center">
                    <button
                        onClick={() => setIsLogin(!isLogin)}
                        className="text-sm text-pink-600 hover:underline"
                    >
                        {isLogin ? "Need an account? Sign Up" : "Already have an account? Login"}
                    </button>
                </div>

                <div className="mt-8 border-t border-gray-200 pt-6">
                    <button
                        onClick={handleGuestLogin}
                        disabled={isSubmitting}
                        className="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center"
                    >
                        {isSubmitting ? <LoadingSpinner size={5}/> : "Continue as Guest"}
                    </button>
                </div>
            </div>
            <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Authentication Notice">
                <p>{modalMessage}</p>
            </Modal>
        </div>
    );
};

const GenerateStoryPage = () => {
    const { userId, isGuest } = useAuthStore();
    const { navigateTo } = useNavStore();
    const { addStory, setLoading: setStoryLoading, setError: setStoryError } = useStoryStore();

    const [prompt, setPrompt] = useState('');
    const [imageFiles, setImageFiles] = useState([]); 
    const [imagePreviews, setImagePreviews] = useState([]); 
    const [isGenerating, setIsGenerating] = useState(false);
    const [modalOpen, setModalOpen] = useState(false);
    const [modalTitle, setModalTitle] = useState('');
    const [modalMessage, setModalMessage] = useState('');
    const fileInputRef = useRef(null);


    const handleImageChange = (e) => {
        const files = Array.from(e.target.files);
        if (files.length > 0) {
            const currentImageCount = imageFiles.length;
            const remainingSlots = 5 - currentImageCount;
            const filesToAdd = files.slice(0, remainingSlots);

            setImageFiles(prevFiles => [...prevFiles, ...filesToAdd]); 

            const newPreviews = [];
            filesToAdd.forEach(file => { 
                const reader = new FileReader();
                reader.onloadend = () => {
                    newPreviews.push({name: file.name, url: reader.result});
                    if (newPreviews.length === filesToAdd.length) {
                         setImagePreviews(prevPreviews => [...prevPreviews, ...newPreviews].slice(0,5)); 
                    }
                };
                reader.readAsDataURL(file);
            });
        }
    };
    
    const clearImages = () => {
        setImageFiles([]);
        setImagePreviews([]);
        if (fileInputRef.current) {
            fileInputRef.current.value = null; 
        }
    };


    const generateStoryText = async (currentPrompt, firstImageBase64Data = null) => {
        let chatHistory = [];
        const parts = [{ text: currentPrompt }];
        if (firstImageBase64Data) {
            parts.push({ inlineData: { mimeType: firstImageBase64Data.type, data: firstImageBase64Data.base64 } });
        }
        chatHistory.push({ role: "user", parts });

        const payload = { contents: chatHistory };
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Gemini API Error:", errorData);
                throw new Error(`Story generation failed: ${errorData.error?.message || response.statusText}`);
            }
            const result = await response.json();
            if (result.candidates && result.candidates.length > 0 &&
                result.candidates[0].content && result.candidates[0].content.parts &&
                result.candidates[0].content.parts.length > 0) {
                return result.candidates[0].content.parts[0].text;
            } else {
                console.error("Unexpected Gemini API response structure:", result);
                throw new Error("Failed to parse story from AI response.");
            }
        } catch (error) {
            console.error("Error generating story text:", error);
            throw error; 
        }
    };

    const generateIllustration = async (textPromptForPage, hasUploadedImages) => {
        let finalPrompt = `A colorful and whimsical children's book illustration for a story page with the text: "${textPromptForPage.substring(0, 150)}..."`;
        if (hasUploadedImages) {
            finalPrompt = `Create a children's book illustration in a style inspired by the user's uploaded image(s), depicting: "${textPromptForPage.substring(0, 120)}..."`;
        }

        const payload = { instances: [{ prompt: finalPrompt }], parameters: { "sampleCount": 1 } };
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${IMAGEN_API_KEY}`;

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Imagen API Error:", errorData);
                throw new Error(`Illustration generation failed: ${errorData.error?.message || response.statusText}`);
            }
            const result = await response.json();
            if (result.predictions && result.predictions.length > 0 && result.predictions[0].bytesBase64Encoded) {
                return `data:image/png;base64,${result.predictions[0].bytesBase64Encoded}`;
            } else {
                console.error("Unexpected Imagen API response structure:", result);
                throw new Error("Failed to parse illustration from AI response.");
            }
        } catch (error) {
            console.error("Error generating illustration:", error);
            return "https://placehold.co/800x600/E0C3FC/5D3A9A?text=Illustration+Error&font=lora";
        }
    };

    const handleGenerateStory = async () => {
        if (!userId && isGuest) {
             setModalTitle("Guest Mode");
             setModalMessage("Story generation for guests is currently for demonstration. Stories won't be saved. Sign up to save your creations!");
             setModalOpen(true);
        } else if (!userId) {
            setModalTitle("Authentication Required");
            setModalMessage("Please log in or sign up to generate and save stories.");
            setModalOpen(true);
            return;
        }

        setIsGenerating(true);
        setStoryLoading(true);
        setStoryError(null);

        try {
            let firstImageBase64Data = null;
            if (imageFiles.length > 0) {
                firstImageBase64Data = await imageFileToBase64(imageFiles[0]); 
            }

            const storyPrompt = prompt || "A fun and adventurous random story for kids about a friendly animal discovering something magical, told in about 5 short paragraphs.";
            const fullStoryText = await generateStoryText(storyPrompt, firstImageBase64Data);
            
            const rawPages = fullStoryText.split(/\n\s*\n/).filter(p => p.trim().length > 30); 
            
            let storyPages = [];
            if (rawPages.length === 0 && fullStoryText.trim().length > 0) { 
                storyPages.push({ text: fullStoryText.trim(), imageUrl: null, pageNum: 1 });
            } else {
                 storyPages = rawPages.slice(0, 5).map((text, index) => ({ 
                    text: text.trim(),
                    imageUrl: null, 
                    pageNum: index + 1,
                }));
            }

            if (storyPages.length === 0) {
                throw new Error("Generated story was too short or couldn't be split into pages.");
            }
            
            setModalTitle("Generating Illustrations...");
            setModalMessage("Hold tight, our little artists are drawing pictures for your story!");
            if(!modalOpen) setModalOpen(true);

            const hasUserUploadedImages = imageFiles.length > 0;
            for (let i = 0; i < storyPages.length; i++) {
                storyPages[i].imageUrl = await generateIllustration(storyPages[i].text, hasUserUploadedImages);
                 setModalMessage(`Generating illustration for page ${i + 1} of ${storyPages.length}...`);
            }
            
            const newStoryData = {
                title: prompt.substring(0, 40).trim() || `A Magical Adventure #${Math.floor(Math.random() * 1000)}`,
                pages: storyPages,
                createdAt: Timestamp.now(), 
                userId: userId, 
                coverImageUrl: storyPages[0]?.imageUrl || "https://placehold.co/300x200/FFC0CB/333333?text=My+Story&font=lora",
            };

            if (userId && !isGuest && db) {
                const docRef = await addDoc(collection(db, `artifacts/${appId}/users/${userId}/stories`), newStoryData);
                addStory({ ...newStoryData, id: docRef.id }); 
                 setModalTitle("Story Created!");
                 setModalMessage("Your magical story is ready!");
                 setTimeout(() => {
                    setModalOpen(false);
                    navigateTo('viewer', docRef.id);
                }, 1500);
            } else if (isGuest) { 
                const guestStoryId = generateRandomId();
                addStory({ ...newStoryData, id: guestStoryId, userId: 'guest-session-active' }); 
                setModalTitle("Story Created (Guest Mode)!");
                setModalMessage("Your magical story is ready! Remember, guest stories are not saved permanently.");
                setTimeout(() => {
                    setModalOpen(false);
                    navigateTo('viewer', guestStoryId);
                }, 1500);
            }

        } catch (error) {
            console.error("Error in story generation pipeline:", error);
            setStoryError(error.message);
            setModalTitle("Generation Failed");
            setModalMessage(`Oops! Something went wrong: ${error.message}. Please try again.`);
            if(!modalOpen) setModalOpen(true);
        } finally {
            setIsGenerating(false);
            setStoryLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4 md:p-8 bg-pink-50 min-h-[calc(100vh-128px)]"> 
            <div className="bg-white p-6 md:p-10 rounded-xl shadow-xl max-w-2xl mx-auto">
                <h2 className="text-3xl font-bold text-center text-purple-600 mb-6">Craft Your Story!</h2>
                
                <button
                    onClick={handleGenerateStory}
                    disabled={isGenerating}
                    className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300 ease-in-out disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center text-lg mb-6"
                >
                    {isGenerating ? (
                        <>
                            <LoadingSpinner size={6} />
                            <span className="ml-2">Creating Magic...</span>
                        </>
                    ) : (
                        <>
                            <Sparkles size={22} className="mr-2" />
                            Generate My Story!
                        </>
                    )}
                </button>
                <p className="text-center text-sm text-gray-600 mb-8 flex items-center justify-center">
                    <Info size={16} className="mr-2 text-indigo-500" />
                    No ideas? No problem! Leave the fields below blank and we'll conjure up a random magical tale for you.
                </p>

                <div className="space-y-6">
                    <div>
                        <label htmlFor="prompt" className="block text-lg font-medium text-gray-700 mb-2">
                            ✨ Share Your Story Idea
                        </label>
                        <textarea
                            id="prompt"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            rows="4"
                            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-shadow"
                            placeholder="e.g., A curious cat who discovers a hidden garden, or a little robot learning to make friends..."
                        />
                        <p className="text-xs text-gray-500 mt-1">What adventure should we embark on? Describe a character, a place, or a magical event!</p>
                    </div>

                    <div>
                        <label htmlFor="imageUpload" className="block text-lg font-medium text-gray-700 mb-2 flex items-center">
                            <Camera size={20} className="mr-2 text-purple-600" /> Spark Visual Ideas (Optional, up to 5 images)
                        </label>
                        <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-purple-400 transition-colors">
                            <div className="space-y-1 text-center">
                                <UploadCloud className="mx-auto h-12 w-12 text-gray-400" />
                                <div className="flex text-sm text-gray-600 justify-center">
                                    <label
                                        htmlFor="imageUploadInput"
                                        className="relative cursor-pointer bg-white rounded-md font-medium text-purple-600 hover:text-purple-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-purple-500 px-1"
                                    >
                                        <span>Upload your pictures</span>
                                        <input 
                                            id="imageUploadInput" 
                                            name="imageUploadInput" 
                                            type="file" 
                                            className="sr-only" 
                                            accept="image/*" 
                                            multiple 
                                            onChange={handleImageChange}
                                            ref={fileInputRef} 
                                        />
                                    </label>
                                    <p className="pl-1 hidden sm:inline">or drag and drop</p>
                                </div>
                                <p className="text-xs text-gray-500">
                                    Drawings, favorite toys, family photos, or special places can inspire unique characters, settings, or plot points! We'll use these to make the story uniquely yours.
                                </p>
                            </div>
                        </div>
                        {imagePreviews.length > 0 && (
                            <div className="mt-4">
                                <p className="text-sm font-medium text-gray-700 mb-2">Your uploaded inspirations ({imagePreviews.length}/5):</p>
                                <div className="flex flex-wrap gap-3">
                                    {imagePreviews.map((preview, index) => (
                                        <div key={index} className="relative group">
                                            <img src={preview.url} alt={`Preview ${preview.name}`} className="h-24 w-24 object-cover rounded-lg border border-gray-300 shadow-sm" />
                                        </div>
                                    ))}
                                </div>
                                <button onClick={clearImages} className="mt-3 text-xs text-red-600 hover:underline font-medium flex items-center">
                                    <Trash2 size={14} className="mr-1"/> Clear all images
                                </button>
                            </div>
                        )}
                         <p className="text-xs text-gray-500 mt-2">The first image you upload gives our AI artist the main idea for the illustrations!</p>
                    </div>
                </div>
            </div>
             <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={modalTitle}>
                <p>{modalMessage}</p>
                {isGenerating && !modalMessage.toLowerCase().includes("illustration") && <div className="mt-4 flex justify-center"><LoadingSpinner /></div>}
            </Modal>
        </div>
    );
};

const PreviousStoriesPage = () => {
    const { userId, isGuest } = useAuthStore();
    const { stories, setStories, isLoading, error, setLoading, setError, deleteStoryState, addStory } = useStoryStore();
    const { navigateTo } = useNavStore();
    const [modalOpen, setModalOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState('');
    const [storyToDelete, setStoryToDelete] = useState(null);

    useEffect(() => {
        if (isGuest) {
            const demoStoryExistsInStore = stories.some(s => s.id === demoStory.id);
            if (!demoStoryExistsInStore) {
                addStory(demoStory); 
            }
            setLoading(false);
            return; 
        }

        if (!userId || !db) {
            setLoading(false); 
            return;
        }
        
        setLoading(true);
        setError(null);
        const storiesRef = collection(db, `artifacts/${appId}/users/${userId}/stories`);
        const q = query(storiesRef); 

        const unsubscribe = onSnapshot(q, (querySnapshot) => {
            let fetchedStories = [];
            querySnapshot.forEach((doc) => {
                fetchedStories.push({ id: doc.id, ...doc.data() });
            });
            fetchedStories.sort((a, b) => (b.createdAt?.toDate() || 0) - (a.createdAt?.toDate() || 0));
            setStories(fetchedStories);
            setLoading(false);
        }, (err) => {
            console.error("Error fetching stories:", err);
            setError(err.message);
            setLoading(false);
            setModalMessage(`Error fetching stories: ${err.message}`);
            setModalOpen(true);
        });

        return () => unsubscribe();
    }, [userId, isGuest, db, appId, setStories, setLoading, setError, addStory, stories]); 


    const confirmDeleteStory = (story) => {
        setStoryToDelete(story);
        setModalMessage(`Are you sure you want to delete the story "${story.title}"? This cannot be undone.`);
        setModalOpen(true);
    };

    const handleDeleteStory = async () => {
        if (!storyToDelete || !userId || isGuest || !db) return;

        try {
            const storyRef = doc(db, `artifacts/${appId}/users/${userId}/stories`, storyToDelete.id);
            await deleteDoc(storyRef);
            deleteStoryState(storyToDelete.id); 
            setModalMessage(`Story "${storyToDelete.title}" deleted successfully.`);
        } catch (err) {
            console.error("Error deleting story:", err);
            setModalMessage(`Error deleting story: ${err.message}`);
        } finally {
            setStoryToDelete(null); 
        }
    };

    if (isLoading && stories.length === 0) { 
        return <div className="flex justify-center items-center h-[calc(100vh-128px)] bg-pink-50"><LoadingSpinner size={12} /></div>;
    }

    return (
        <div className="container mx-auto p-4 md:p-8 bg-pink-50 min-h-[calc(100vh-128px)]">
            <h2 className="text-3xl font-bold text-center text-purple-600 mb-8">My Story Collection</h2>
            {isGuest && stories.length > 0 && stories.some(s => !s.isDemo) && ( 
                <p className="text-center text-sm text-orange-600 bg-orange-100 p-3 rounded-md mb-6">
                    You are in Guest Mode. Your created stories are only available for this session. The demo story is always here for inspiration!
                </p>
            )}
            {stories.length === 0 && !isLoading && (
                <div className="text-center py-12">
                    <BookOpen size={64} className="mx-auto text-gray-400 mb-4" />
                    <p className="text-xl text-gray-500 mb-4">
                        {isGuest ? "No stories created in this session yet. Check out the demo!" : "Your storybook shelf is empty!"}
                    </p>
                    <button
                        onClick={() => navigateTo('generate')}
                        className="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all"
                    >
                        <Sparkles size={20} className="inline mr-2" />
                        Create Your First Story
                    </button>
                </div>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {stories.map((story) => (
                    <div key={story.id} className={`bg-white rounded-xl shadow-lg overflow-hidden transform transition-all hover:shadow-2xl hover:scale-105 duration-300 ease-in-out flex flex-col ${story.isDemo ? 'border-2 border-purple-300' : ''}`}>
                        <img
                            src={story.coverImageUrl || "https://placehold.co/300x200/E0C3FC/5D3A9A?text=Story&font=lora"}
                            alt={story.title}
                            className="w-full h-48 object-cover cursor-pointer"
                            onClick={() => navigateTo('viewer', story.id)}
                            onError={(e) => e.target.src = "https://placehold.co/300x200/FFC0CB/333333?text=Image+Error&font=lora"}
                        />
                        <div className="p-4 flex flex-col flex-grow">
                            <h3 className="text-lg font-semibold text-purple-700 mb-1 truncate" title={story.title}>
                                {story.title} {story.isDemo && <span className="text-xs text-purple-500">(Demo)</span>}
                            </h3>
                            <p className="text-xs text-gray-500 mb-3">
                                Created: {story.createdAt?.toDate ? story.createdAt.toDate().toLocaleDateString() : 'Recently'}
                            </p>
                            <button
                                onClick={() => navigateTo('viewer', story.id)}
                                className="mt-auto w-full bg-pink-500 hover:bg-pink-600 text-white text-sm font-medium py-2 px-3 rounded-md transition-colors flex items-center justify-center"
                            >
                                <BookOpen size={16} className="mr-2" /> Read Story
                            </button>
                            {!isGuest && !story.isDemo && ( 
                                <button
                                    onClick={() => confirmDeleteStory(story)}
                                    className="mt-2 w-full bg-red-500 hover:bg-red-600 text-white text-sm font-medium py-2 px-3 rounded-md transition-colors flex items-center justify-center"
                                >
                                    <Trash2 size={16} className="mr-2" /> Delete
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            <Modal isOpen={modalOpen} onClose={() => { setModalOpen(false); if(storyToDelete) setStoryToDelete(null); }} title={storyToDelete ? "Confirm Deletion" : "Story Collection Notice"}>
                <p>{modalMessage}</p>
                {storyToDelete && (
                    <div className="mt-4 flex justify-end space-x-3">
                        <button onClick={() => { setModalOpen(false); setStoryToDelete(null); }} className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300">Cancel</button>
                        <button onClick={handleDeleteStory} className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600">Delete</button>
                    </div>
                )}
            </Modal>
        </div>
    );
};


const StoryViewerPage = () => {
    const { storyIdToView } = useNavStore();
    const { stories, currentStory, setCurrentStory, isLoading, error, setLoading, setError } = useStoryStore();
    const { userId, isGuest } = useAuthStore();

    const [currentPageIndex, setCurrentPageIndex] = useState(0); 
    const [isSpeaking, setIsSpeaking] = useState(false);
    const utteranceRef = useRef(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState('');

    useEffect(() => {
        if (storyIdToView === demoStory.id) {
            setCurrentStory(demoStory);
            setCurrentPageIndex(0);
            setLoading(false);
            return;
        }

        const storyFromList = stories.find(s => s.id === storyIdToView);
        if (storyFromList) {
            setCurrentStory(storyFromList);
            setCurrentPageIndex(0);
            setLoading(false);
            return;
        }

        if (storyIdToView && userId && !isGuest && db) {
            setLoading(true);
            setError(null);
            const storyRef = doc(db, `artifacts/${appId}/users/${userId}/stories`, storyIdToView);
            getDoc(storyRef).then(docSnap => {
                if (docSnap.exists()) {
                    setCurrentStory({ id: docSnap.id, ...docSnap.data() });
                    setCurrentPageIndex(0);
                } else {
                    setError("Story not found.");
                    setModalMessage("Oops! We couldn't find that story.");
                    setModalOpen(true);
                }
                setLoading(false);
            }).catch(err => {
                console.error("Error fetching single story:", err);
                setError(err.message);
                setLoading(false);
                setModalMessage(`Error loading story: ${err.message}`);
                setModalOpen(true);
            });
        } else if (isGuest && !storyFromList) {
            setError("Story not found in this session.");
            setModalMessage("This guest story is not available.");
            setModalOpen(true);
            setLoading(false);
        } else {
            setLoading(false);
        }

        return () => {
            if (window.speechSynthesis && window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                setIsSpeaking(false);
            }
        };
    }, [storyIdToView, userId, isGuest, stories, setCurrentStory, setLoading, setError, appId]);

    const handleSpeak = () => {
        if (!currentStory || !currentStory.pages || currentStory.pages.length === 0) return;

        if ('speechSynthesis' in window) {
            if (window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
                setIsSpeaking(false);
                return;
            }

            const leftPageText = currentStory.pages[currentPageIndex]?.text;
            const rightPageText = (currentPageIndex + 1 < currentStory.pages.length) ? currentStory.pages[currentPageIndex + 1]?.text : null;
            
            let textToSpeak = "";
            if (leftPageText) textToSpeak += leftPageText;
            if (rightPageText) textToSpeak += " " + rightPageText; 

            if (!textToSpeak.trim()) {
                setModalMessage("No text to read on the current page(s).");
                setModalOpen(true);
                return;
            }

            utteranceRef.current = new SpeechSynthesisUtterance(textToSpeak);
            utteranceRef.current.lang = 'en-US';
            utteranceRef.current.rate = 0.9;
            utteranceRef.current.pitch = 1.1;
            utteranceRef.current.onstart = () => setIsSpeaking(true);
            utteranceRef.current.onend = () => setIsSpeaking(false);
            utteranceRef.current.onerror = (event) => {
                console.error('SpeechSynthesisUtterance.onerror', event);
                setIsSpeaking(false);
                setModalMessage(`Text-to-speech error: ${event.error}`);
                setModalOpen(true);
            };
            window.speechSynthesis.speak(utteranceRef.current);
        } else {
            setModalMessage('Sorry, your browser does not support text-to-speech.');
            setModalOpen(true);
        }
    };

    const nextPage = () => {
        if (currentStory && (currentPageIndex + 2 < currentStory.pages.length)) {
            setCurrentPageIndex(currentPageIndex + 2);
            if (window.speechSynthesis.speaking) window.speechSynthesis.cancel(); setIsSpeaking(false);
        }
    };

    const prevPage = () => {
        if (currentPageIndex - 2 >= 0) {
            setCurrentPageIndex(currentPageIndex - 2);
            if (window.speechSynthesis.speaking) window.speechSynthesis.cancel(); setIsSpeaking(false);
        }
    };

    if (isLoading || (!currentStory && isLoading)) {
        return <div className="flex justify-center items-center h-[calc(100vh-128px)] bg-purple-50"><LoadingSpinner size={12} /></div>; 
    }
    
    if (error && !currentStory) {
        return (
            <div className="text-center p-8 bg-purple-50 min-h-[calc(100vh-128px)] flex flex-col justify-center items-center">
                <FileText size={64} className="mx-auto text-gray-400 mb-4" />
                <p className="text-xl text-red-500">Error: {error}</p>
                <p className="text-sm text-gray-400">Could not load the story.</p>
            </div>
        );
    }

    if (!currentStory || !currentStory.pages || currentStory.pages.length === 0) {
        return (
            <div className="text-center p-8 bg-purple-50 min-h-[calc(100vh-128px)] flex flex-col justify-center items-center">
                <FileText size={64} className="mx-auto text-gray-400 mb-4" />
                <p className="text-xl text-gray-500">No story content to display.</p>
            </div>
        );
    }

    const leftPageData = currentStory.pages[currentPageIndex];
    const rightPageData = (currentPageIndex + 1 < currentStory.pages.length) ? currentStory.pages[currentPageIndex + 1] : null;
    const totalPages = currentStory.pages.length;
    
    const PageDisplay = ({ pageData, side }) => {
        if (!pageData) {
            if (side === 'right') { // Only render empty placeholder for right page in double-page view
                 return <div className={`w-full md:w-1/2 h-full bg-gray-100 md:border-l border-gray-200`}></div>;
            }
            return null; 
        }
        return (
            <div 
                className={`w-full md:w-1/2 h-full relative flex flex-col justify-end items-center bg-cover bg-center ${side === 'right' ? 'md:border-l' : ''} border-gray-200`}
                style={{ backgroundImage: `url(${pageData.imageUrl || `https://placehold.co/800x600/E0C3FC/5D3A9A?text=Page+${pageData.pageNum}&font=lora`})` }}
                onError={(e) => { e.target.style.backgroundImage = `url(https://placehold.co/800x600/FFC0CB/333333?text=Image+Error&font=lora)`}}
            >
                <div className="absolute inset-0 bg-black bg-opacity-10 pointer-events-none"></div> {/* Subtle overlay for text contrast if needed */}
                <div className="w-11/12 max-h-[45%] overflow-y-auto p-2 sm:p-3 md:p-4 bg-white bg-opacity-80 backdrop-blur-sm rounded-lg shadow-lg mb-4 mx-auto">
                    <p className="text-gray-800 leading-relaxed text-xs sm:text-sm md:text-base whitespace-pre-line font-serif">
                        {pageData.text}
                    </p>
                </div>
            </div>
        );
    };
    
    const isSinglePageView = totalPages === 1; 

    return (
        <div className="container mx-auto p-2 sm:p-4 flex flex-col items-center justify-center bg-purple-50 min-h-[calc(100vh-128px)]"> 
            <h2 className="text-2xl sm:text-3xl font-bold text-center text-pink-600 mb-3 sm:mb-4">{currentStory.title} {currentStory.isDemo && <span className="text-lg text-purple-500">(Demo)</span>}</h2>
            
            <div className={`w-full max-w-xs sm:max-w-2xl md:max-w-4xl lg:max-w-5xl bg-white rounded-xl shadow-2xl overflow-hidden ${isSinglePageView ? 'aspect-[3/4] sm:aspect-square md:aspect-[4/3]' : 'aspect-[4/3] sm:aspect-[2/1] md:aspect-[8/3]'} relative flex flex-col`}>
                <div className="flex-grow flex flex-col md:flex-row overflow-hidden">
                   <PageDisplay pageData={leftPageData} side="left" />
                    {!isSinglePageView && (
                        <>
                            <div className="hidden md:block w-1 sm:w-2 bg-gray-300 shadow-inner"></div> {/* Gutter */}
                            <PageDisplay pageData={rightPageData} side="right" />
                        </>
                    )}
                </div>

                <div className="bg-gray-100 p-2 sm:p-3 border-t border-gray-200 flex items-center justify-between">
                    <button
                        onClick={prevPage}
                        disabled={currentPageIndex === 0}
                        className="p-2 rounded-full bg-pink-500 text-white hover:bg-pink-600 disabled:bg-gray-300 transition-colors"
                        aria-label="Previous Page"
                    >
                        <ChevronLeft size={18} sm:size={20} />
                    </button>
                    
                    <div className="flex items-center space-x-2 sm:space-x-3">
                        <button
                            onClick={handleSpeak}
                            className={`p-2 rounded-full text-white transition-colors ${isSpeaking ? 'bg-red-500 hover:bg-red-600' : 'bg-purple-500 hover:bg-purple-600'}`}
                            aria-label={isSpeaking ? "Stop Reading" : "Read Aloud"}
                        >
                            <Volume2 size={18} sm:size={20} />
                        </button>
                        <span className="text-xs sm:text-sm text-gray-600">
                            {totalPages === 0 ? "Page 0 of 0" : 
                             isSinglePageView || !rightPageData ? `Page ${leftPageData?.pageNum || 0} of ${totalPages}` : 
                             `Pages ${leftPageData?.pageNum || 0}-${rightPageData?.pageNum || 0} of ${totalPages}`}
                        </span>
                    </div>

                    <button
                        onClick={nextPage}
                        disabled={isSinglePageView || !rightPageData || (currentPageIndex + 2 >= totalPages && leftPageData?.pageNum === totalPages -1 && rightPageData?.pageNum === totalPages) || (leftPageData?.pageNum === totalPages && !rightPageData) }
                        className="p-2 rounded-full bg-pink-500 text-white hover:bg-pink-600 disabled:bg-gray-300 transition-colors"
                        aria-label="Next Page"
                    >
                        <ChevronRight size={18} sm:size={20} />
                    </button>
                </div>
            </div>
             <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Story Viewer Notice">
                <p>{modalMessage}</p>
            </Modal>
        </div>
    );
};


const App = () => {
    const { setUser, setLoading, isLoading: authLoading, user: authUser } = useAuthStore();
    const { currentPage } = useNavStore(); 
    const [isFirebaseReady, setIsFirebaseReady] = useState(false);

    useEffect(() => {
        if (!auth) {
            console.warn("Firebase Auth not available on initial App mount.");
            setLoading(false); 
            setIsFirebaseReady(false);
            return;
        }
        
        setIsFirebaseReady(true);
        setLoading(true); 

        const attemptSignIn = async () => {
            try {
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token && !auth.currentUser) {
                    console.log("Attempting sign in with custom token...");
                    await signInWithCustomToken(auth, __initial_auth_token);
                } else {
                     console.log("No custom token or user already present. Relying on onAuthStateChanged / existing session.");
                }
            } catch (error) { 
                console.error("Error with initial auth token sign in:", error);
            }
        };

        attemptSignIn();

        const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
            console.log("Auth state changed, user:", firebaseUser ? firebaseUser.uid : null);
            setUser(firebaseUser); 
        });
        
        return () => unsubscribe();
    }, [setUser, setLoading]); 

    if (authLoading || !isFirebaseReady) {
        return (
            <div className="flex flex-col justify-center items-center min-h-screen bg-gradient-to-br from-purple-200 via-pink-200 to-indigo-200 text-pink-500">
                <LoadingSpinner size={16} />
                <p className="mt-4 text-lg font-semibold">Sparking up the magic...</p>
                {!isFirebaseReady && <p className="text-sm text-red-500 mt-2">Waiting for Firebase to connect...</p>}
            </div>
        );
    }

    let pageComponent;
    if (!authUser && currentPage !== 'auth') { 
        pageComponent = <AuthPage />;
    } else {
        switch (currentPage) {
            case 'auth':
                pageComponent = <AuthPage />;
                break;
            case 'generate':
                pageComponent = authUser ? <GenerateStoryPage /> : <AuthPage />;
                break;
            case 'previous':
                pageComponent = authUser ? <PreviousStoriesPage /> : <AuthPage />;
                break;
            case 'viewer':
                pageComponent = <StoryViewerPage />;
                break;
            default:
                pageComponent = <AuthPage />;
        }
    }
    
    const showNavbar = currentPage !== 'auth' || (currentPage === 'auth' && authUser);


    return (
        <div className="font-sans antialiased text-gray-800 bg-gray-50 flex flex-col min-h-screen">
            {showNavbar && <Navbar />}
            <main className={`flex-grow ${showNavbar ? 'pt-16' : ''}`}> 
                {pageComponent}
            </main>
            <footer className="text-center p-4 text-xs text-gray-500 border-t border-gray-200">
                StorySpark AI &copy; {new Date().getFullYear()} - Create magical stories! (App ID: {appId})
                {auth.currentUser && <span className="block text-xs">User ID: {auth.currentUser.uid}</span>}
            </footer>
        </div>
    );
};

export default App;

