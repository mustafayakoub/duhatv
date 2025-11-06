import React from 'react'
import { Button } from '../shared/Button'

interface TopBarProps {
  onSettingsClick: () => void
  onSearchClick: () => void
}

export const TopBar: React.FC<TopBarProps> = ({ onSettingsClick, onSearchClick }) => {
  return (
    <div className="h-12 bg-white border-b-2 border-golden-200 flex items-center justify-between px-4 shadow-sm">
      {/* اليمين: العنوان */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-gradient-to-br from-golden-400 to-golden-600 rounded-lg flex items-center justify-center text-white font-bold">
          ب
        </div>
        <h1 className="text-lg font-bold text-golden-800 font-arabic">بصائر القرآن الكريم</h1>
      </div>

      {/* اليسار: الأدوات */}
      <div className="flex items-center gap-2">
        {/* زر البحث */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onSearchClick}
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          }
        >
          <span className="font-arabic">بحث</span>
        </Button>

        {/* زر الإعدادات */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onSettingsClick}
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          }
        >
          <span className="font-arabic">إعدادات</span>
        </Button>
      </div>
    </div>
  )
}
