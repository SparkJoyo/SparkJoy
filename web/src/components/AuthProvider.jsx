import React, { createContext, useState } from 'react'

export const AuthContext = createContext()

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)

    const login = (username) => {
        const userData = { username, id: Date.now() }
        setUser(userData)
    }

    const loginAsGuest = () => {
        setUser({ username: 'Guest', id: 'guest-' + Date.now() })
    }

    const logout = () => {
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, login, loginAsGuest, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthProvider
