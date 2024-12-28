import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './App.css'
import Main from './components/main'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Main />
  </StrictMode>,
)
