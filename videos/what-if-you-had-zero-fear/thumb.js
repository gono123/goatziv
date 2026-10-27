// THE THUMBNAIL: one frame, drawn for a phone-sized YouTube thumbnail. Two words, one calm kid,
// one roaring monster, and the fear meter at zero.   node make-thumb.js -> out/thumbnail.png
(function () {
  const G = globalThis.G, K = globalThis.K, Studio = globalThis.Studio;
  const W = G.W, H = G.H, INK = K.INK;
  Studio.film({
    duration: 5,
    fadeOut: 0,
    post: { paper: 0.5, vignette: 0.35, grain: 0.2 },
    draw(ctx, t) {
      K.sky(ctx, '#2A2050', '#E8704A');
      G.rays(ctx, 640, 640, { n: 30, r0: 160, r1: 1900, color: 'rgba(255,214,120,0.22)', lw: 34, seed: 7 });
      // the monster looms on the right, roaring
      K.monster(ctx, 1480, 1180, 2.15, t, { look: -1, arms: 1 });
      // Sam: arms crossed, not bothered, a spider on his shoulder
      K.sam(ctx, { x: 640, y: 1250, s: 2.0, crossArms: true, mouth: 'smirk', eyes: 'normal', look: 0.25 });
      K.spider(ctx, 775, 650, 0.8, t, { rot: 0.3 });
      // the words
      ctx.save(); ctx.translate(960, 190); ctx.rotate(-0.035);
      G.text(ctx, 'ZERO FEAR?', 0, 0, { size: 230, align: 'center', fam: 'Bungee', weight: 400, color: '#FFD23F', stroke: INK, strokeW: 22, boil: 0 });
      ctx.restore();
      // the meter, pinned at zero
      K.meter(ctx, 230, 860, 150, 0, { seed: 9 });
      K.stamp(ctx, '0%', 230, 1050, 1, 0, { size: 110, color: '#6BBF7A', strokeW: 12 });
    },
  });
})();
