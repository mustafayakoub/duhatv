import React from 'react'

interface SelectOption {
  value: string | number
  label: string
}

interface SelectProps {
  label?: string
  value: string | number
  onChange: (value: string | number) => void
  options: SelectOption[]
  className?: string
}

export const Select: React.FC<SelectProps> = ({ label, value, onChange, options, className = '' }) => {
  return (
    <div className={className}>
      {label && <label className="block text-sm font-medium text-gray-700 font-arabic mb-2">{label}</label>}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-2 bg-white border-2 border-golden-300 rounded-lg focus:border-golden-500 focus:outline-none transition-colors font-arabic text-right"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )
}
