'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Plus, History, Settings, LogOut } from 'lucide-react';
import { useGenerationStore } from '@/lib/store';

export function Sidebar() {
  const generations = useGenerationStore((state) => state.generations);

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col border-r border-gray-800">
      {/* Logo */}
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold">Script Gen</h1>
        <p className="text-xs text-gray-400">Unified Generator</p>
      </div>

      {/* New Chat Button */}
      <div className="p-4 border-b border-gray-800">
        <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
          <Plus className="w-4 h-4 mr-2" />
          New Generation
        </Button>
      </div>

      {/* History */}
      <div className="flex-1 overflow-hidden flex flex-col p-4 border-b border-gray-800">
        <div className="flex items-center gap-2 mb-3">
          <History className="w-4 h-4" />
          <span className="text-sm font-semibold">Recent</span>
        </div>

        <ScrollArea className="flex-1">
          <div className="space-y-2">
            {generations.slice(-5).map((gen) => (
              <button
                key={gen.id}
                className="w-full text-left p-3 rounded hover:bg-gray-800 transition-colors text-sm text-gray-300 hover:text-white truncate"
                title={gen.prompt}
              >
                <div className="font-medium truncate">{gen.skill}</div>
                <div className="text-xs text-gray-500 truncate">
                  {gen.prompt.substring(0, 40)}...
                </div>
              </button>
            ))}

            {generations.length === 0 && (
              <div className="text-xs text-gray-500 text-center py-8">
                No generations yet
              </div>
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800 space-y-2">
        <Button variant="ghost" className="w-full justify-start text-gray-300 hover:text-white">
          <Settings className="w-4 h-4 mr-2" />
          Settings
        </Button>
        <Button variant="ghost" className="w-full justify-start text-gray-300 hover:text-white">
          <LogOut className="w-4 h-4 mr-2" />
          Logout
        </Button>
      </div>
    </div>
  );
}
