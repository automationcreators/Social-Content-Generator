'use client';

import React from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Play, Zap, Briefcase, MessageCircle, Mail, Image } from 'lucide-react';

interface SkillSelectorProps {
  selectedSkill: string;
  onSkillChange: (skill: string) => void;
}

const skills = [
  {
    id: 'youtube',
    name: 'YouTube Pillar Scripts',
    icon: Play,
    description: 'Long-form viral YouTube scripts',
    status: 'active' as const,
  },
  {
    id: 'tiktok',
    name: 'TikTok/Short-form',
    icon: Zap,
    description: 'Quick viral scripts for TikTok, Reels, Shorts',
    status: 'active' as const,
  },
  {
    id: 'linkedin',
    name: 'LinkedIn Posts',
    icon: Briefcase,
    description: 'Professional thought leadership content',
    status: 'active' as const,
  },
  {
    id: 'twitter',
    name: 'Twitter/Threads',
    icon: MessageCircle,
    description: 'Tweets and thread scripts',
    status: 'planning' as const,
  },
  {
    id: 'email',
    name: 'Email Sequences',
    icon: Mail,
    description: 'Email marketing scripts',
    status: 'planning' as const,
  },
  {
    id: 'instagram',
    name: 'Instagram Captions',
    icon: Image,
    description: 'Instagram post captions',
    status: 'planning' as const,
  },
];

export function SkillSelector({
  selectedSkill,
  onSkillChange,
}: SkillSelectorProps) {
  const selected = skills.find((s) => s.id === selectedSkill);
  const Icon = selected?.icon || Play;

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select Skill
      </label>
      <Select value={selectedSkill} onValueChange={onSkillChange}>
        <SelectTrigger className="w-full">
          <div className="flex items-center gap-2">
            <Icon className="w-4 h-4" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {skills.map((skill) => {
            const SkillIcon = skill.icon;
            return (
              <SelectItem
                key={skill.id}
                value={skill.id}
                disabled={skill.status === 'planning'}
              >
                <div className="flex items-center gap-2">
                  <SkillIcon className="w-4 h-4" />
                  <div>
                    <div className="font-medium">{skill.name}</div>
                    <div className="text-xs text-gray-500">{skill.description}</div>
                  </div>
                  {skill.status === 'planning' && (
                    <span className="ml-2 text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                      Coming soon
                    </span>
                  )}
                </div>
              </SelectItem>
            );
          })}
        </SelectContent>
      </Select>
    </div>
  );
}
