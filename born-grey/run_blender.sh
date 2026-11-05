#!/bin/sh
# Headless Blender (bpy) with software OpenGL for Eevee.
export EGL_PLATFORM=surfaceless LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe MESA_GL_VERSION_OVERRIDE=4.5
exec "${BPY_PYTHON:-python3.11}" "$@" 2>&1 | grep -vE "EGL Error|^Fra:|^$|Saved:|Time: "
