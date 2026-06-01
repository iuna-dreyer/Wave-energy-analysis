import numpy as np
import math
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd




ds = xr.open_dataset('../data/raw/portugal_wave_data.nc')

height_ds, h = ds['VHM0'], 'height'
period_ds, p = ds['VTM02'], 'period'
direction_ds, d = ds['VMDR'], 'direction'




def unit_analysis():
    
    text = '\nDATA OVERVIEW\n\n\n'
    
    # Time -----------------------------------------------------------------------------------------
    text += 'Time:\n------------------------------\n------------------------------\n'
    
    time_units = ds.time.dtype
    
    start_time = ds.time.min().values
    end_time = ds.time.max().values
    
    duration = ds.time.max() - ds.time.min()
    duration_days = float((duration / np.timedelta64(1, 'D')))
    
    sampling_intervals, sampling_interval_counts = np.unique(np.diff(ds.time), return_counts=True)
    main_interval = sampling_intervals[np.argmax(sampling_interval_counts)] # the most frequent
    sampling_interval_hours = main_interval / np.timedelta64(1, 'h')
    sampling_gaps_Q = False if len(sampling_intervals)==1 else True # as these are integers, there are no rounding errors
    
    timestamps_number = len(ds.time)
    
    text += f"Units for time: {time_units} (nanoseconds)\n\n"
    text += f"Sampling range: {pd.Timestamp(start_time).strftime('%Y-%m-%d %H:%M')} - {pd.Timestamp(end_time).strftime('%Y-%m-%d %H:%M')}  ({duration_days} days)\n\n"
    text += f"Sampling interval: {sampling_interval_hours} hours\n\n"
    text += f"There are {'' if sampling_gaps_Q else 'no '}gaps in the sampling and a total of {timestamps_number} timestamps.\n\n\n"
    
    
    # Space ------------------------------------------------------------------------------------------
    text += 'Space:\n------------------------------\n------------------------------\n'
    
    lat_units = ds.latitude.attrs['unit_long']
    long_units = ds.longitude.attrs['unit_long']
    
    lat_northmost = ds.latitude.max().values
    lat_southmost = ds.latitude.min().values
    long_westmost = ds.longitude.min().values
    long_eastmost = ds.longitude.max().values
    
    km_lat = 111.03 # approximate km per degree latitude at 40ºN
    km_long = 85.39 # approximate km per degree longitude at 40ºN
    
    lat_range = abs(lat_northmost-lat_southmost) * km_lat
    long_range = abs(long_westmost-long_eastmost) * km_long
    
    lat_spacings, lat_spacing_counts = np.unique(np.diff(ds.latitude), return_counts=True)
    long_spacings, long_spacing_counts = np.unique(np.diff(ds.longitude), return_counts=True)
    dlat, dlong = lat_spacings[np.argmax(lat_spacing_counts)], long_spacings[np.argmax(long_spacing_counts)]
    main_lat_spacing = np.average(lat_spacings[np.abs(lat_spacings-dlat)<0.1*dlat], weights=lat_spacing_counts[np.abs(lat_spacings-dlat)<0.1*dlat]) # overcomplicated way to get a mode and then averaging...
    main_long_spacing = np.average(long_spacings[np.abs(long_spacings-dlong)<0.1*dlong], weights=long_spacing_counts[np.abs(long_spacings-dlong)<0.1*dlong]) # overcomplicated way to get a mode and then averaging...
    lat_spacing_km = main_lat_spacing * km_lat
    long_spacing_km = main_long_spacing * km_long
    lat_gaps_Q = False if (len(lat_spacings)==1 or max(lat_spacings)-min(lat_spacings)<0.1*min(lat_spacings)) else True # if there is only one value, or the values don't differ in more than 10% of the smallest
    long_gaps_Q = False if (len(long_spacings)==1 or max(long_spacings)-min(long_spacings)<0.1*min(long_spacings)) else True 
    
    lat_number_points = len(ds.latitude)
    long_number_points = len(ds.longitude)
    
    text += f"Units for latitude: {lat_units}\n"
    text += f"Units for longitude: {long_units}\n\n"
    text += f"Latitude range: {lat_southmost} - {lat_northmost}  ({lat_range}km total)\n"
    text += f"Longitude range: {long_westmost} - {long_eastmost}  ({long_range}km total)\n\n"
    text += f"Latitude spacing: {lat_spacing_km}km\n"
    text += f"Longitude spacing: {long_spacing_km}km\n\n"
    text += f"There are {'' if lat_gaps_Q else 'no '}gaps in the latitude sampling and a total of {lat_number_points} points.\n"
    text += f"There are {'' if long_gaps_Q else 'no '}gaps in the longitude sampling and a total of {long_number_points} points.\n\n\n"
    

    # Wave height -------------------------------------------------------------------------------------
    text += 'Wave Height:\n------------------------------\n------------------------------\n'
    
    h_name = height_ds.attrs.get('long_name')
    h_units = height_ds.attrs.get('units')
    
    h_max = float(height_ds.max())
    time_idx, lat_idx, long_idx = np.unravel_index(height_ds.argmax().item(),height_ds.shape)
    h_max_time = height_ds.time[time_idx].values
    h_max_lat = float(height_ds.latitude[lat_idx])
    h_max_long = float(height_ds.longitude[long_idx])
    
    h_min = float(height_ds.min())
    time_idx, lat_idx, long_idx = np.unravel_index(height_ds.argmin().item(),height_ds.shape)
    h_min_time = height_ds.time[time_idx].values
    h_min_lat = float(height_ds.latitude[lat_idx])
    h_min_long = float(height_ds.longitude[long_idx])
    
    percentiles = height_ds.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    h_p5  = float(percentiles.sel(quantile=0.05))
    h_p25 = float(percentiles.sel(quantile=0.25))
    h_p50 = float(percentiles.sel(quantile=0.50))
    h_p75 = float(percentiles.sel(quantile=0.75))
    h_p95 = float(percentiles.sel(quantile=0.95))
    
    h_mean = float(height_ds.mean())
    h_std = float(height_ds.std())
    
    h_n_missing = int(height_ds.isnull().sum())
    h_pct_missing = 100 * h_n_missing / height_ds.size
    
    text += f"Variable long name: {h_name}\n\n"
    text += f"Height units: {h_units} (meters)\n\n"
    text += f"The maximum wave height is {h_max}{h_units} and occurs at (lat,long,time) coordinates ({h_max_lat}, {h_max_long}, {pd.Timestamp(h_max_time).strftime("%Y-%m-%d %H:%M")}).\n\n"
    text += f"The minimum wave height is {h_min}{h_units} and occurs at (lat,long,time) coordinates ({h_min_lat}, {h_min_long}, {pd.Timestamp(h_min_time).strftime("%Y-%m-%d %H:%M")}).\n\n"
    text += 'Percentiles (0.05, 0.25, 0.50, 0.75, 0.95)\n'
    text += f"Wave Height ({h_p5:.2f}, {h_p25:.2f}, {h_p50:.2f}, {h_p75:.2f}, {h_p95:.2f})\n\n"
    text += f"Mean: {h_mean}\n"
    text += f"Standard deviation: {h_std}\n\n"
    text += f"{h_n_missing} values missing ({h_pct_missing:.2f}%)\n\n\n"
    
    height_ds.max(dim=['latitude','longitude']).plot()
    filename = 'Output/maximum_wave_height_over_time.pdf'
    plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()
    
    # Wave period -------------------------------------------------------------------------------------
    text += 'Wave Period:\n------------------------------\n------------------------------\n'
    
    p_name = period_ds.attrs.get('long_name')
    p_units = period_ds.attrs.get('units')
    
    p_max = float(period_ds.max())
    time_idx, lat_idx, long_idx = np.unravel_index(period_ds.argmax().item(),period_ds.shape)
    p_max_time = period_ds.time[time_idx].values
    p_max_lat = float(period_ds.latitude[lat_idx])
    p_max_long = float(period_ds.longitude[long_idx])
    
    p_min = float(period_ds.min())
    time_idx, lat_idx, long_idx = np.unravel_index(period_ds.argmin().item(),period_ds.shape)
    p_min_time = period_ds.time[time_idx].values
    p_min_lat = float(period_ds.latitude[lat_idx])
    p_min_long = float(period_ds.longitude[long_idx])
    
    percentiles = period_ds.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    p_p5  = float(percentiles.sel(quantile=0.05))
    p_p25 = float(percentiles.sel(quantile=0.25))
    p_p50 = float(percentiles.sel(quantile=0.50))
    p_p75 = float(percentiles.sel(quantile=0.75))
    p_p95 = float(percentiles.sel(quantile=0.95))
    
    p_mean = float(period_ds.mean())
    p_std = float(period_ds.std())
    
    p_n_missing = int(period_ds.isnull().sum())
    p_pct_missing = 100 * p_n_missing / period_ds.size
    
    text += f"Variable long name: {p_name}\n\n"
    text += f"Period units: {p_units} (seconds)\n\n"
    text += f"The maximum wave period is {p_max}{p_units} and occurs at (lat,long,time) coordinates ({p_max_lat}, {p_max_long}, {pd.Timestamp(p_max_time).strftime('%Y-%m-%d %H:%M')}).\n\n"
    text += f"The minimum wave period is {p_min}{p_units} and occurs at (lat,long,time) coordinates ({p_min_lat}, {p_min_long}, {pd.Timestamp(p_min_time).strftime('%Y-%m-%d %H:%M')}).\n\n"
    text += 'Percentiles (0.05, 0.25, 0.50, 0.75, 0.95)\n'
    text += f"Wave Period ({p_p5:.2f}, {p_p25:.2f}, {p_p50:.2f}, {p_p75:.2f}, {p_p95:.2f})\n\n"
    text += f"Mean: {p_mean}\n"
    text += f"Standard deviation: {p_std}\n\n"
    text += f"{p_n_missing} values missing ({p_pct_missing:.2f}%)\n\n\n"
    
    
    
    
    # Wave direction -------------------------------------------------------------------------------------
    text += 'Wave Direction:\n------------------------------\n------------------------------\n'
    
    d_name = direction_ds.attrs.get('long_name')
    d_units = direction_ds.attrs.get('units')
    
    sin_mean = float(np.sin(np.deg2rad(direction_ds)).mean())
    cos_mean = float(np.cos(np.deg2rad(direction_ds)).mean())
    d_mean = np.rad2deg(np.arctan2(sin_mean, cos_mean))% 360
    d_std = float(np.std(((direction_ds - d_mean + 180) % 360) - 180))
    
    d_n_missing = int(direction_ds.isnull().sum())
    d_pct_missing = 100 * d_n_missing / direction_ds.size
    
    
    text += f"Variable long name: {d_name}\n\n"
    text += f"Direction units: {d_units}, 0°=N, 90°=E\n\n"
    text += f"Mean direction: {d_mean:.2f}°\n"
    text += f"Circular standard deviation: {d_std:.2f}°\n\n"
    text += f"{d_n_missing} values missing ({d_pct_missing:.2f}%)\n\n\n"
    
    
    plt.hist(direction_ds.values.ravel(), bins=np.arange(0, 361, 10))
    plt.xlabel('Direction (deg)')
    plt.ylabel('Count')
    filename = 'Output/directions_histogram.pdf'
    plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()
    
    
    # Comparing variables -------------------------------------------------------------------------------------
    text += 'Comparing Missing Values:\n------------------------------\n------------------------------\n'
    
    
    h_missing = height_ds.isnull()
    p_missing = period_ds.isnull()
    d_missing = direction_ds.isnull()
    
    h_changing_cells = (h_missing.any(dim='time') & ~h_missing.all(dim='time')).sum().item()
    p_changing_cells = (p_missing.any(dim='time') & ~p_missing.all(dim='time')).sum().item()
    d_changing_cells = (d_missing.any(dim='time') & ~d_missing.all(dim='time')).sum().item()
    
    n_diff_h_p = (h_missing != p_missing).sum().item()
    n_missing_d_notmissing_h_p = (d_missing & ~(h_missing & p_missing)).sum().item()
    n_notmissing_d_missing_h_p = (~d_missing & (h_missing & p_missing)).sum().item()
    
    
    text += f"Direction has {h_n_missing-d_n_missing} less missing values than height and period.\n\n"
    
    text += f"{h_changing_cells} points have valid height values at some times and missing at others.\n"
    text += f"{p_changing_cells} points have valid period values at some times and missing at others.\n"
    text += f"{d_changing_cells} points have valid direction values at some times and missing at others.\n\n"
    
    
    text += f"{n_diff_h_p} points have missing height and valid period or vice-versa.\n"
    text += f"{n_missing_d_notmissing_h_p} points have missing direction and valid height and period.\n"
    text += f"{n_notmissing_d_missing_h_p} points have valid direction and missing height and period.\n\n"
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    
    height_ds.isnull().isel(time=0).plot(ax=ax[0],add_colorbar=False)
    ax[0].set_title('height missing')
    
    (direction_ds.notnull() & height_ds.isnull()).isel(time=0).plot(ax=ax[1],add_colorbar=False)
    ax[1].set_title('direction valid, height missing')
    
    filename = 'Output/missing_values.pdf'
    fig.savefig(filename, format='pdf', bbox_inches='tight')
    
    with open("Output/Overview.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)




def au():
    print('\n\n\nhigh waves associated with specific directions?\n------------------------------------------------------------------------')
    




def plot_timegrid(var=h, i_tstart=0, i_tend=len(ds.time)-1, nplots=24, ncols=6):
    
    label = 'Significant Wave Height (m)' if var=='height' else 'Mean Wave Period (s)' if var=='period' else 'Wave Direction (degrees)'
    var_ds = height_ds if var=='height' else period_ds if var=='period' else direction_ds
    
    selected_times = ds.time[np.linspace(i_tstart, i_tend, nplots, dtype=int)]
    
    nrows = math.ceil(nplots / ncols)
    fig, axes = plt.subplots(nrows=nrows,ncols=ncols,figsize=(14, 12),subplot_kw={'projection': ccrs.PlateCarree()},constrained_layout=True)
    axes = axes.flatten()
    
    vmin = float(var_ds.min())
    vmax = float(var_ds.max())
    
    for ax, t in zip(axes, selected_times):
        data = var_ds.sel(time=t)
        if var=='direction':
            step = 7
            lon = data.longitude.values[::step]
            lat = data.latitude.values[::step]
            arrow_length = 3/4 * min(np.mean(np.diff(lon)), np.mean(np.diff(lat)))
            theta = np.deg2rad(data.values[::step,::step]+180) # +180 because the value is where the waves come from and I want to plot where thay move towards
            pcm = ax.quiver(lon, lat, arrow_length*np.sin(theta), arrow_length*np.cos(theta),data.values[::step,::step],cmap='hsv',scale_units='xy',scale=1,clim=(0, 360))
        else:
            pcm = ax.pcolormesh(ds.longitude,ds.latitude,data,shading='auto',cmap='viridis',vmin=vmin,vmax=vmax)
        
        ax.set_title(str(t.values)[:16])
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        ax.coastlines()
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
    
    for ax in axes[len(selected_times):]:
        ax.remove()
    
    fig.colorbar(pcm,ax=axes.tolist(),shrink=0.95,label=label)
    filename = f"Output/wave_{var}_evolution_{i_tstart}-{i_tend}_{nplots}.pdf"
    fig.savefig(filename, format='pdf', bbox_inches='tight')
    print(f"Saved figure to: {filename}")
    
    plt.show()











