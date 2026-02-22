#!/usr/bin/env python3
"""
Unified Script Generator API Server

FastAPI backend for the unified script generation UI.
Wraps existing Python agents and provides REST API endpoints.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import uuid
import json
import logging
import asyncio
import sys
import importlib.util

# Setup paths first
HOME = Path.home()
PROJECT_ROOT = HOME / "Documents/claudec/active/Social-Content-Generator"
PILLAR_SCRIPTS_PATH = PROJECT_ROOT / "pillar_scripts"
sys.path.insert(0, str(PILLAR_SCRIPTS_PATH))
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Unified Script Generator API",
    description="API for generating scripts across multiple platforms",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup additional paths
BACKEND_DIR = PROJECT_ROOT / "backend"
GENERATIONS_DIR = BACKEND_DIR / "generations"
GENERATIONS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class GenerationRequest(BaseModel):
    """Request model for script generation"""
    prompt: str
    skill: str  # 'youtube', 'tiktok', 'linkedin', etc.
    style: Optional[str] = None  # 'contrarian', 'authority', 'transformation'
    tone: Optional[str] = None  # 'professional', 'casual', 'humorous'
    length: Optional[str] = "medium"  # 'short', 'medium', 'long'
    file_path: Optional[str] = None
    additional_context: Optional[str] = None


class GenerationResponse(BaseModel):
    """Response model for generation"""
    id: str
    status: str  # 'processing', 'completed', 'failed'
    prompt: str
    skill: str
    generated_script: Optional[str] = None
    created_at: str
    updated_at: str
    metadata: Dict[str, Any] = {}


class FeedbackRequest(BaseModel):
    """Request model for feedback on generation"""
    generation_id: str
    feedback: str
    style_changes: Optional[Dict[str, str]] = None
    regenerate: bool = True


class VersionResponse(BaseModel):
    """Response model for script version"""
    version_id: str
    generation_id: str
    script_content: str
    created_at: str
    feedback: Optional[str] = None
    is_current: bool


class ExportRequest(BaseModel):
    """Request model for exporting generation"""
    generation_id: str
    format: str  # 'markdown', 'pdf', 'google_drive'
    include_metadata: bool = True


# ============================================================================
# IN-MEMORY STORAGE (Phase 1 - will move to database)
# ============================================================================

generations_store: Dict[str, Dict] = {}
versions_store: Dict[str, List[Dict]] = {}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def import_unified_generator():
    """Import the unified generator script"""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT / "pillar_scripts"))

    try:
        # Import as module
        spec = __import__(
            'importlib.util'
        ).util.spec_from_file_location(
            "unified_generator",
            PROJECT_ROOT / "pillar_scripts/unified_gemini_youtube_generator.py"
        )
        unified_generator = __import__(
            'importlib.util'
        ).util.module_from_spec(spec)
        spec.loader.exec_module(unified_generator)
        return unified_generator
    except Exception as e:
        logger.error(f"Error importing unified generator: {e}")
        return None


def generate_script_youtube(prompt: str, context: Optional[List] = None) -> str:
    """Generate YouTube script using unified generator"""
    try:
        # Import from pillar_scripts directly (path already added to sys.path)
        from unified_gemini_youtube_generator import (
            YouTubeScriptGenerator,
            GeminiFileSearchManager
        )

        logger.info(f"Generating YouTube script for prompt: {prompt[:50]}...")

        # Get context
        file_search = GeminiFileSearchManager()
        context = file_search.get_script_context(prompt)

        # Generate
        generator = YouTubeScriptGenerator()
        script = generator.generate_script(prompt, context)

        logger.info(f"Successfully generated script, length: {len(script)} chars")
        return script
    except Exception as e:
        logger.error(f"Error generating YouTube script: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")


def generate_script_tiktok(prompt: str) -> str:
    """Generate TikTok/short-form script"""
    return f"""# TikTok Script: {prompt}

## Hook (3 seconds)
Stop [pain point]. Here's the [solution] that actually works.

## Body (12 seconds)
[Key insight 1]
[Key insight 2]
[Call to action]

## Closing CTA
Follow for more [topic] tips!

---
Generated: {datetime.now().isoformat()}
"""


def generate_script_linkedin(prompt: str) -> str:
    """Generate LinkedIn post script"""
    return f"""# LinkedIn Post: {prompt}

[Opening Hook - Start with curiosity or insight]

[Body - 3-5 key points with real examples]

1. [First insight with proof]
2. [Second insight with proof]
3. [Third insight with proof]

[Closing - Ask engagement question or call to action]

---
Generated: {datetime.now().isoformat()}
"""


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }


@app.get("/skills")
async def list_skills():
    """List available script generation skills"""
    return {
        "skills": [
            {
                "id": "youtube",
                "name": "YouTube Pillar Scripts",
                "description": "Long-form viral YouTube scripts with proven hooks",
                "icon": "play-circle",
                "status": "active"
            },
            {
                "id": "tiktok",
                "name": "TikTok/Short-form",
                "description": "Quick viral scripts for TikTok, Reels, Shorts",
                "icon": "zap",
                "status": "active"
            },
            {
                "id": "linkedin",
                "name": "LinkedIn Posts",
                "description": "Professional thought leadership content",
                "icon": "briefcase",
                "status": "active"
            },
            {
                "id": "twitter",
                "name": "Twitter/Threads",
                "description": "Tweets and thread scripts",
                "icon": "message-circle",
                "status": "planning"
            },
            {
                "id": "email",
                "name": "Email Sequences",
                "description": "Email marketing scripts",
                "icon": "mail",
                "status": "planning"
            },
            {
                "id": "instagram",
                "name": "Instagram Captions",
                "description": "Instagram post captions and carousels",
                "icon": "image",
                "status": "planning"
            }
        ]
    }


@app.post("/generate", response_model=GenerationResponse)
async def generate_script(request: GenerationRequest, background_tasks: BackgroundTasks):
    """
    Generate a script based on prompt and selected skill

    Supports:
    - Text prompt input
    - File path input
    - Additional context
    - Style and tone customization
    """
    generation_id = str(uuid.uuid4())

    try:
        logger.info(f"Starting generation {generation_id} with skill={request.skill}")

        # Route to appropriate generator
        if request.skill == "youtube":
            script = generate_script_youtube(request.prompt)
        elif request.skill == "tiktok":
            script = generate_script_tiktok(request.prompt)
        elif request.skill == "linkedin":
            script = generate_script_linkedin(request.prompt)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown skill: {request.skill}")

        # Store generation
        generation = {
            "id": generation_id,
            "prompt": request.prompt,
            "skill": request.skill,
            "style": request.style,
            "tone": request.tone,
            "script": script,
            "created_at": datetime.now().isoformat(),
            "status": "completed",
            "versions": [
                {
                    "version_id": str(uuid.uuid4()),
                    "content": script,
                    "created_at": datetime.now().isoformat(),
                    "is_current": True,
                    "feedback": None
                }
            ]
        }

        generations_store[generation_id] = generation

        # Schedule Google Drive upload in background
        background_tasks.add_task(upload_to_drive, generation_id, script)

        logger.info(f"Generation {generation_id} completed")

        return GenerationResponse(
            id=generation_id,
            status="completed",
            prompt=request.prompt,
            skill=request.skill,
            generated_script=script,
            created_at=generation["created_at"],
            updated_at=generation["created_at"],
            metadata={"style": request.style, "tone": request.tone}
        )

    except Exception as e:
        logger.error(f"Generation {generation_id} failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generations/{generation_id}", response_model=GenerationResponse)
async def get_generation(generation_id: str):
    """Get a specific generation"""
    if generation_id not in generations_store:
        raise HTTPException(status_code=404, detail="Generation not found")

    gen = generations_store[generation_id]

    return GenerationResponse(
        id=gen["id"],
        status=gen["status"],
        prompt=gen["prompt"],
        skill=gen["skill"],
        generated_script=gen.get("script"),
        created_at=gen["created_at"],
        updated_at=gen.get("updated_at", gen["created_at"]),
        metadata={"style": gen.get("style"), "tone": gen.get("tone")}
    )


@app.get("/generations/{generation_id}/versions")
async def get_versions(generation_id: str) -> List[VersionResponse]:
    """Get all versions of a generation"""
    if generation_id not in generations_store:
        raise HTTPException(status_code=404, detail="Generation not found")

    gen = generations_store[generation_id]
    versions = gen.get("versions", [])

    return [
        VersionResponse(
            version_id=v["version_id"],
            generation_id=generation_id,
            script_content=v["content"],
            created_at=v["created_at"],
            feedback=v.get("feedback"),
            is_current=v.get("is_current", False)
        )
        for v in versions
    ]


@app.post("/generations/{generation_id}/feedback")
async def submit_feedback(generation_id: str, feedback: FeedbackRequest):
    """Submit feedback and optionally regenerate with changes"""
    if generation_id not in generations_store:
        raise HTTPException(status_code=404, detail="Generation not found")

    gen = generations_store[generation_id]

    # Store feedback on current version
    if gen["versions"]:
        gen["versions"][-1]["feedback"] = feedback.feedback

    # Regenerate if requested
    if feedback.regenerate:
        try:
            # Apply style/tone changes
            prompt = gen["prompt"]
            if feedback.style_changes:
                if "tone" in feedback.style_changes:
                    gen["tone"] = feedback.style_changes["tone"]
                if "style" in feedback.style_changes:
                    gen["style"] = feedback.style_changes["style"]

            # Regenerate script
            if gen["skill"] == "youtube":
                new_script = generate_script_youtube(prompt)
            elif gen["skill"] == "tiktok":
                new_script = generate_script_tiktok(prompt)
            elif gen["skill"] == "linkedin":
                new_script = generate_script_linkedin(prompt)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown skill: {gen['skill']}")

            # Add new version
            new_version = {
                "version_id": str(uuid.uuid4()),
                "content": new_script,
                "created_at": datetime.now().isoformat(),
                "is_current": True,
                "feedback": feedback.feedback
            }

            # Mark previous as not current
            for v in gen["versions"]:
                v["is_current"] = False

            gen["versions"].append(new_version)
            gen["updated_at"] = datetime.now().isoformat()

            return {
                "status": "regenerated",
                "generation_id": generation_id,
                "new_version_id": new_version["version_id"],
                "script": new_script
            }

        except Exception as e:
            logger.error(f"Regeneration failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return {"status": "feedback_recorded", "generation_id": generation_id}


@app.post("/export")
async def export_generation(request: ExportRequest):
    """Export a generation in various formats"""
    if request.generation_id not in generations_store:
        raise HTTPException(status_code=404, detail="Generation not found")

    gen = generations_store[request.generation_id]
    script = gen["script"]

    if request.format == "google_drive":
        # Upload to Google Drive
        return await upload_to_drive(request.generation_id, script)
    elif request.format == "markdown":
        return {"format": "markdown", "content": script}
    elif request.format == "pdf":
        # In Phase 2: implement PDF export
        return {"format": "pdf", "status": "coming_soon"}
    else:
        raise HTTPException(status_code=400, detail=f"Unknown format: {request.format}")


async def upload_to_drive(generation_id: str, script: str):
    """Upload generated script to Google Drive"""
    try:
        import sys
        sys.path.insert(0, str(PROJECT_ROOT / "pillar_scripts"))
        from upload_to_gdrive import authenticate, upload_file, FOLDER_ID

        # Save script to temp file
        temp_file = GENERATIONS_DIR / f"temp_{generation_id}.md"
        with open(temp_file, 'w') as f:
            f.write(script)

        # Upload
        service = authenticate()
        upload_file(service, temp_file, FOLDER_ID)

        # Cleanup
        temp_file.unlink()

        logger.info(f"Generation {generation_id} uploaded to Google Drive")
        return {"status": "uploaded", "generation_id": generation_id}

    except Exception as e:
        logger.error(f"Google Drive upload failed: {e}")
        return {"status": "upload_failed", "error": str(e)}


@app.get("/generations")
async def list_generations():
    """List all generations (with pagination in Phase 2)"""
    return {
        "total": len(generations_store),
        "generations": [
            {
                "id": gen["id"],
                "prompt": gen["prompt"][:100] + "...",
                "skill": gen["skill"],
                "created_at": gen["created_at"],
                "status": gen["status"],
                "versions_count": len(gen.get("versions", []))
            }
            for gen in generations_store.values()
        ]
    }


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting Unified Script Generator API")
    logger.info(f"Generations directory: {GENERATIONS_DIR}")
    logger.info(f"Available skills: YouTube, TikTok, LinkedIn")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Unified Script Generator API")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
