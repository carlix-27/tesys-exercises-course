import os

import pygame

_ANIM_FPS = {"idle": 3, "attack": 10, "hurt": 6, "death": 4, "greet": 6}
_LOOPING_STATES = {"idle"}
_AUTO_RETURN_STATES = {"attack", "hurt", "greet"}


class Animator:
    def __init__(self, frames, fps=6, loop=True):
        self.frames = frames
        self.fps = max(1, fps)
        self.loop = loop
        self.time = 0.0

    @property
    def frame_duration(self):
        return 1.0 / self.fps

    @property
    def total_duration(self):
        return self.frame_duration * len(self.frames)

    @property
    def finished(self):
        return (not self.loop) and self.time >= self.total_duration - 1e-6

    def reset(self):
        self.time = 0.0

    def update(self, dt):
        self.time += dt
        if self.loop:
            total = self.total_duration
            if total > 0:
                self.time %= total
        else:
            self.time = min(self.time, self.total_duration - 1e-6)

    def current_frame(self):
        idx = int(self.time / self.frame_duration)
        idx = max(0, min(idx, len(self.frames) - 1))
        return self.frames[idx]


class CharacterSprite:
    """Plays idle/attack/hurt/death frame sequences loaded from a character
    folder (files named e.g. attack_0.png, attack_1.png, ...). `has_art`
    tells the caller whether any frames were found at all, so a missing
    folder degrades to no sprite instead of crashing."""

    def __init__(self, folder, flip=False, scale=2.0):
        self.flip = flip
        self.scale = scale
        self.animations = {}
        if folder and os.path.isdir(folder):
            for state, fps in _ANIM_FPS.items():
                frames = self._load_frames(folder, state)
                if frames:
                    self.animations[state] = Animator(frames, fps=fps, loop=(state in _LOOPING_STATES))
        self.has_art = bool(self.animations)
        self.state = "idle" if "idle" in self.animations else None

    @staticmethod
    def _load_frames(folder, prefix):
        frames = []
        i = 0
        while True:
            path = os.path.join(folder, f"{prefix}_{i}.png")
            if not os.path.isfile(path):
                break
            frames.append(pygame.image.load(path).convert_alpha())
            i += 1
        return frames

    def play(self, state):
        if not self.has_art:
            return
        if state not in self.animations:
            state = "idle"
        if state not in self.animations:
            return
        if self.state != state:
            self.state = state
            self.animations[state].reset()

    def update(self, dt):
        if not self.has_art:
            return
        anim = self.animations.get(self.state)
        if anim is None:
            return
        anim.update(dt)
        if anim.finished and self.state in _AUTO_RETURN_STATES:
            self.play("idle")

    def duration_of(self, state):
        anim = self.animations.get(state)
        return anim.total_duration if anim else None

    def get_surface(self):
        anim = self.animations.get(self.state) or self.animations.get("idle")
        if anim is None:
            return None
        frame = anim.current_frame()
        if self.flip:
            frame = pygame.transform.flip(frame, True, False)
        if self.scale != 1:
            w, h = frame.get_size()
            frame = pygame.transform.scale(frame, (int(w * self.scale), int(h * self.scale)))
        return frame

    def draw(self, surface, feet_pos):
        """Draws the current frame anchored by its bottom-center (feet on the ground).

        Hit feedback comes from the art itself (the "hurt" frames bake in a
        translucent impact card) rather than a programmatic flash overlay.
        """
        frame = self.get_surface()
        if frame is None:
            return None
        rect = frame.get_rect(midbottom=feet_pos)
        surface.blit(frame, rect)
        return rect
