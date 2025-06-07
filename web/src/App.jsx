import { Routes, Route } from 'react-router-dom'
import AuthProvider from './components/AuthProvider'
import Login from './components/Login'
import StoryGenerator from './components/StoryGenerator'
import StoryLibrary from './components/StoryLibrary'
import StoryViewer from './components/StoryViewer'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/create" element={<StoryGenerator />} />
        <Route path="/library" element={<StoryLibrary />} />
        <Route path="/story/:id" element={<StoryViewer />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
