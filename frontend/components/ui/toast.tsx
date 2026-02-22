import React from 'react'
import { X } from 'lucide-react'

interface ToastProps {
  message: string
  type: 'success' | 'error' | 'info'
  onClose?: () => void
}

const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
  }[type]

  return (
    <div className={`${bgColor} text-white px-4 py-3 rounded-md flex items-center justify-between`}>
      <span>{message}</span>
      {onClose && (
        <button onClick={onClose} className="ml-4">
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  )
}

Toast.success = (message: string) => {
  console.log(`✓ ${message}`)
}

Toast.error = (message: string) => {
  console.error(`✗ ${message}`)
}

Toast.info = (message: string) => {
  console.info(`ℹ ${message}`)
}

const Toaster = () => <div id="toast-container" />

const useToast = () => ({
  toast: (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    const typeStr = type.toUpperCase()
    console.log(`[${typeStr}] ${message}`)
  },
})

export { Toast, Toaster, useToast }
