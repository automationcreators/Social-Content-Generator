'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Github, HelpCircle, Settings, User } from 'lucide-react';

export function Header() {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Unified Script Generator</h1>
        <p className="text-sm text-gray-600">Generate scripts across platforms with AI</p>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" title="Help">
          <HelpCircle className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" title="Settings">
          <Settings className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" title="User">
          <User className="w-5 h-5" />
        </Button>
      </div>
    </div>
  );
}
