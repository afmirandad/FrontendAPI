/**
 * Network Interconnected Particle System
 * Creates an animated background with connected particles
 */

class ParticleNetwork {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: null, y: null, radius: 150 };
        
        // Configuration
        this.config = {
            particleCount: 80,
            particleSpeed: 0.5,
            particleSize: 2,
            connectionDistance: 150,
            mouseConnectionDistance: 200,
            particleColor: 'rgba(129, 140, 248, 0.8)',
            lineColor: 'rgba(99, 102, 241, 0.2)',
            mouseLineColor: 'rgba(139, 92, 246, 0.4)'
        };
        
        this.init();
    }
    
    init() {
        this.resize();
        this.createParticles();
        this.setupEventListeners();
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        this.particles = [];
        const particleCount = Math.floor(
            (this.canvas.width * this.canvas.height) / 15000 * this.config.particleCount / 80
        );
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * this.config.particleSpeed,
                vy: (Math.random() - 0.5) * this.config.particleSpeed,
                radius: Math.random() * this.config.particleSize + 1
            });
        }
    }
    
    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.resize();
            this.createParticles();
        });
        
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
        
        window.addEventListener('mouseout', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }
    
    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = this.config.particleColor;
        this.ctx.fill();
    }
    
    drawLine(x1, y1, x2, y2, opacity, color) {
        this.ctx.beginPath();
        this.ctx.strokeStyle = color || this.config.lineColor;
        this.ctx.globalAlpha = opacity;
        this.ctx.lineWidth = 1;
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
        this.ctx.globalAlpha = 1;
    }
    
    updateParticle(particle) {
        // Update position
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        // Bounce off walls
        if (particle.x < 0 || particle.x > this.canvas.width) {
            particle.vx = -particle.vx;
            particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
        }
        if (particle.y < 0 || particle.y > this.canvas.height) {
            particle.vy = -particle.vy;
            particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
        }
        
        // Mouse interaction
        if (this.mouse.x !== null && this.mouse.y !== null) {
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < this.mouse.radius) {
                const force = (this.mouse.radius - distance) / this.mouse.radius;
                const angle = Math.atan2(dy, dx);
                particle.vx -= Math.cos(angle) * force * 0.05;
                particle.vy -= Math.sin(angle) * force * 0.05;
            }
        }
        
        // Limit speed
        const speed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
        const maxSpeed = this.config.particleSpeed * 2;
        if (speed > maxSpeed) {
            particle.vx = (particle.vx / speed) * maxSpeed;
            particle.vy = (particle.vy / speed) * maxSpeed;
        }
    }
    
    connectParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.config.connectionDistance) {
                    const opacity = 1 - (distance / this.config.connectionDistance);
                    this.drawLine(
                        this.particles[i].x,
                        this.particles[i].y,
                        this.particles[j].x,
                        this.particles[j].y,
                        opacity * 0.5,
                        this.config.lineColor
                    );
                }
            }
            
            // Connect to mouse
            if (this.mouse.x !== null && this.mouse.y !== null) {
                const dx = this.mouse.x - this.particles[i].x;
                const dy = this.mouse.y - this.particles[i].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.config.mouseConnectionDistance) {
                    const opacity = 1 - (distance / this.config.mouseConnectionDistance);
                    this.drawLine(
                        this.particles[i].x,
                        this.particles[i].y,
                        this.mouse.x,
                        this.mouse.y,
                        opacity * 0.8,
                        this.config.mouseLineColor
                    );
                }
            }
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw particles
        this.particles.forEach(particle => {
            this.updateParticle(particle);
            this.drawParticle(particle);
        });
        
        // Draw connections
        this.connectParticles();
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particle network when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particles-canvas');
    if (canvas) {
        new ParticleNetwork(canvas);
    }
});
