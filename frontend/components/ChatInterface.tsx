'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { SkillSelector } from './SkillSelector';
import { OutputPanel } from './OutputPanel';
import { Toast } from '@/components/ui/toast';
import { useGenerationStore } from '@/lib/store';
import { api } from '@/lib/api';
import {
  Upload,
  Send,
  FileText,
  Loader,
  ArrowUp,
  Copy,
  Download,
  Share2,
  Zap
} from 'lucide-react';

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  generationId?: string;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [selectedSkill, setSelectedSkill] = useState('youtube');
  const [isLoading, setIsLoading] = useState(false);
  const [inputMode, setInputMode] = useState<'text' | 'file' | 'path'>('text');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePath, setFilePath] = useState('');
  const [currentGeneration, setCurrentGeneration] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const generations = useGenerationStore((state) => state.generations);
  const addGeneration = useGenerationStore((state) => state.addGeneration);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setInputMode('file');
      setInput(`Uploaded: ${file.name}`);
    }
  };

  // Handle file path input
  const handleFilePathChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilePath(e.target.value);
    setInput(`File: ${e.target.value}`);
  };

  // Generate script
  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) {
      Toast.error('Please enter a prompt');
      return;
    }

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Start loading
    setIsLoading(true);

    try {
      // Call API to generate
      const response = await api.generateScript({
        prompt: input,
        skill: selectedSkill,
        file_path: filePath || undefined,
        additional_context: selectedFile
          ? `File uploaded: ${selectedFile.name}`
          : undefined,
      });

      // Add to store
      addGeneration(response);
      setCurrentGeneration(response);

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: response.generated_script,
        timestamp: new Date(),
        generationId: response.id,
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Reset inputs
      setInput('');
      setSelectedFile(null);
      setFilePath('');

      Toast.success(`${selectedSkill} script generated!`);
    } catch (error: any) {
      Toast.error(error.message || 'Failed to generate script');

      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: `Error: ${error.message || 'Generation failed'}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle quick actions
  const quickPrompts = [
    { label: 'AI Automation', text: 'Generate a YouTube script about AI automation for SMBs' },
    { label: 'Business Growth', text: 'Create a LinkedIn post about scaling with AI' },
    { label: 'Short Form', text: 'Make a TikTok script about productivity hacks' },
  ];

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full space-y-6 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold text-gray-900">
                Unified Script Generator
              </h2>
              <p className="text-gray-600 text-lg">
                Generate scripts across platforms with context-aware AI
              </p>
            </div>

            {/* Quick Prompts */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full max-w-2xl">
              {quickPrompts.map((prompt) => (
                <button
                  key={prompt.label}
                  onClick={() => {
                    setInput(prompt.text);
                  }}
                  className="p-3 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all text-left"
                >
                  <div className="font-medium text-gray-900">{prompt.label}</div>
                  <div className="text-sm text-gray-600">{prompt.text.substring(0, 40)}...</div>
                </button>
              ))}
            </div>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full max-w-3xl text-left">
              <div className="p-4 rounded-lg bg-blue-50 border border-blue-200">
                <div className="font-medium text-blue-900 mb-1">🔍 Smart Search</div>
                <div className="text-sm text-blue-700">Find relevant past scripts automatically</div>
              </div>
              <div className="p-4 rounded-lg bg-green-50 border border-green-200">
                <div className="font-medium text-green-900 mb-1">⚡ Multiple Skills</div>
                <div className="text-sm text-green-700">YouTube, TikTok, LinkedIn, and more</div>
              </div>
              <div className="p-4 rounded-lg bg-purple-50 border border-purple-200">
                <div className="font-medium text-purple-900 mb-1">📤 Auto Upload</div>
                <div className="text-sm text-purple-700">Syncs to Google Drive automatically</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-2xl rounded-lg p-4 ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white text-gray-900 border border-gray-200 rounded-bl-none'
                  }`}
                >
                  {message.type === 'assistant' ? (
                    <div className="prose prose-sm max-w-none">
                      <pre className="bg-gray-50 p-3 rounded overflow-x-auto text-sm">
                        {message.content}
                      </pre>
                    </div>
                  ) : (
                    <div className="text-white">{message.content}</div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-900 border border-gray-200 rounded-lg p-4 rounded-bl-none">
                  <div className="flex items-center space-x-2">
                    <Loader className="w-4 h-4 animate-spin" />
                    <span>Generating {selectedSkill} script...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4 space-y-3">
        {/* Skill Selector */}
        <div className="flex gap-2 items-center">
          <SkillSelector
            selectedSkill={selectedSkill}
            onSkillChange={setSelectedSkill}
          />
        </div>

        {/* Input Tabs */}
        <Tabs value={inputMode} onValueChange={(v: any) => setInputMode(v)}>
          <TabsList>
            <TabsTrigger value="text">Text</TabsTrigger>
            <TabsTrigger value="file">File Upload</TabsTrigger>
            <TabsTrigger value="path">File Path</TabsTrigger>
          </TabsList>

          <TabsContent value="text" className="mt-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your prompt... E.g., 'Create a YouTube script about building AI agents'"
              className="h-24 resize-none"
              disabled={isLoading}
            />
          </TabsContent>

          <TabsContent value="file" className="mt-2">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-500 transition-colors cursor-pointer">
              <input
                type="file"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
                accept=".txt,.md,.pdf,.docx"
              />
              <label htmlFor="file-upload" className="cursor-pointer block">
                <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <div className="text-sm font-medium">
                  {selectedFile ? selectedFile.name : 'Click to upload or drag file'}
                </div>
                <div className="text-xs text-gray-500">
                  Supported: TXT, MD, PDF, DOCX
                </div>
              </label>
            </div>
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Add additional context..."
              className="h-16 mt-2 resize-none"
              disabled={isLoading}
            />
          </TabsContent>

          <TabsContent value="path" className="mt-2">
            <Input
              value={filePath}
              onChange={handleFilePathChange}
              placeholder="/path/to/your/file.txt"
              className="mb-2"
              disabled={isLoading}
            />
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your prompt..."
              className="h-20 resize-none"
              disabled={isLoading}
            />
          </TabsContent>
        </Tabs>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button
            onClick={handleGenerate}
            disabled={isLoading || !input.trim()}
            className="flex-1 h-10 bg-blue-600 hover:bg-blue-700 text-white"
          >
            {isLoading ? (
              <>
                <Loader className="w-4 h-4 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Send className="w-4 h-4 mr-2" />
                Generate Script
              </>
            )}
          </Button>

          {currentGeneration && (
            <>
              <Button
                variant="outline"
                size="icon"
                onClick={() => {
                  navigator.clipboard.writeText(currentGeneration.generated_script);
                  Toast.success('Copied to clipboard');
                }}
                title="Copy to clipboard"
              >
                <Copy className="w-4 h-4" />
              </Button>

              <Button
                variant="outline"
                size="icon"
                onClick={() => {
                  const element = document.createElement('a');
                  element.setAttribute(
                    'href',
                    'data:text/plain;charset=utf-8,' +
                      encodeURIComponent(currentGeneration.generated_script)
                  );
                  element.setAttribute('download', `script-${Date.now()}.md`);
                  element.style.display = 'none';
                  document.body.appendChild(element);
                  element.click();
                  document.body.removeChild(element);
                  Toast.success('Downloaded');
                }}
                title="Download as markdown"
              >
                <Download className="w-4 h-4" />
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
