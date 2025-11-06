import React from 'react'

interface CheckboxProps {
  label: string
  checked: boolean
  onChange: (checked: boolean) => void
  description?: string
}

export const Checkbox: React.FC<CheckboxProps> = ({ label, checked, onChange, description }) => {
  return (
    <label className="flex items-start gap-3 cursor-pointer group">
      <div className="relative flex items-center justify-center mt-0.5">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          className="sr-only peer"
        />
        <div className="w-5 h-5 border-2 border-golden-400 rounded peer-checked:bg-golden-500 peer-checked:border-golden-500 transition-all duration-200 group-hover:border-golden-500">
          {checked && (
            <svg
              className="w-full h-full text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </div>
      </div>
      <div className="flex-1">
        <div className="text-gray-800 font-medium font-arabic">{label}</div>
        {description && <div className="text-sm text-gray-600 font-arabic mt-0.5">{description}</div>}
      </div>
    </label>
  )
}
