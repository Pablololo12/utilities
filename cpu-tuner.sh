#!/bin/bash

# Created by Pablo
# https://pablololo12.github.io

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

echo -e "\033[0;36m========================================================================\033[0m"
echo -e "\033[0;41m ██████╗██████╗ ██╗   ██╗   ████████╗██╗   ██╗███╗   ██╗███████╗██████╗ \033[0m"
echo -e "\033[0;42m██╔════╝██╔══██╗██║   ██║   ╚══██╔══╝██║   ██║████╗  ██║██╔════╝██╔══██╗\033[0m"
echo -e "\033[0;43m██║     ██████╔╝██║   ██║█████╗██║   ██║   ██║██╔██╗ ██║█████╗  ██████╔╝\033[0m"
echo -e "\033[0;44m██║     ██╔═══╝ ██║   ██║╚════╝██║   ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗\033[0m"
echo -e "\033[0;45m╚██████╗██║     ╚██████╔╝      ██║   ╚██████╔╝██║ ╚████║███████╗██║  ██║\033[0m"
echo -e "\033[0;46m ╚═════╝╚═╝      ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\033[0m"
echo -e "\033[0;36m========================================================================\033[0m"

echo -e "\nPress h for help"

while true;
do
	echo -n "Option: "
	read option

	case $option in
		g)
			error=0
			echo -n "New governor: "
			read gov
			echo -n "Setting new governor..."
			for file in `ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`
			do
				echo $gov >$file 2>/dev/null
				if [ $? -ne 0 ]; then
					error=1
					break
				fi
			done
			if [ $? = 0 -a $error = 0 ];
			then
				echo -e "[\033[0;92mOK\033[0m]"
			else
				echo -e "[\033[0;41mERROR\033[0m]"
			fi
		;;
		f)
			error=0
			echo -n "Frequency in KHz: "
			read freq
			echo -n "Setting frequency to $freq..."
			for file in `ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_setspeed`
			do
				echo $freq >$file 2>/dev/null
				if [ $? -ne 0 ]; then
					error=1
					break
				fi
			done
			if [ $? = 0 -a $error = 0 ];
			then
				echo -e "[\033[0;92mOK\033[0m]"
			else
				echo -e "[\033[0;41mERROR\033[0m]"
			fi
		;;
		lg)
			echo `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors`
		;;
		lf)
			echo `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies`
		;;
		cg)
			echo `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
		;;
		cf)
			echo `cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq`
		;;
		h)
			echo -e "g - change governor\nf - change frequency\nlg - list governors\nlf - list availables frequencies"
			echo -e "cg - current governor\ncf - current frequency\nh - help\nq - exit"
		;;
		q)
			break
		;;
		*)
			echo "$option not recognised"
		;;
	esac
done