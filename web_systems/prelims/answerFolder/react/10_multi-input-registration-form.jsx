// Problem 10: Multi-Input Registration Form
// Category: React.js — Difficulty: Medium — Type: Build
// 
// **Problem:**
// Build a form with two inputs: `name` and `email`. Store both in a single state object `{name: '', email: ''}`. On submit, prevent the default form action and log the current state to the console.
// 
// 
// **Example:**
// Typing "Ana" in the name field and "ana@mail.com" in the email field, then pressing submit, logs `{name: "Ana", email: "ana@mail.com"}`.
// 
// 
// **Constraints:**
// - Use one `useState` object.
// - Each input must update its own field in the object.
// 
// 
// **Prelims topic:**
// form state, controlled components, event handlers.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here

import React, { useState } from 'react';


export default function App(){
    const [formData, setFormData] = useState({
        name: '',
        email: ''
    })
    return (
        <form>
            <input 
                type="text" 
                placeholder="Name" 
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
            />
            <input 
                type="email" 
                placeholder="Email" 
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
            <button type="submit">Submit</button>
        </form>
    )
}
