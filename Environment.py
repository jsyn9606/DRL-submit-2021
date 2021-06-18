import pandas as pd
import numpy as np
import gym
import math
import random



class MCS(gym.Env):
    
    def __init__(self):
        
        self.grid = np.zeros([10,10])
        self.action_space = 4
        self.state_space = 9
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        
    
    def reset(self):
        self.state = np.zeros([8])
        self.grid = np.zeros([10,10])
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        state = self.get_state()
        return state
    
    
    def get_state(self):
        state = np.zeros(8)
        
        if self.battery == 0:
            if self.car[0] > self.depot[0]:
                state[0] = 1
            if self.car[1] < self.depot[1]:
                state[1] = 1
            if self.car[0] < self.depot[0]:
                state[2] = 1
            if self.car[1] > self.depot[1]:
                state[3] = 1
        
        else:
            if self.car[0] > self.customer[0]:
                state[0] = 1
            if self.car[1] < self.customer[1]:
                state[1] = 1
            if self.car[0] < self.customer[0]:
                state[2] = 1
            if self.car[1] > self.customer[1]:
                state[3] = 1
            
        if self.car[0] == 0:
            state[4] = 1
        if self.car[1] == 9:
            state[5] = 1
        if self.car[0] == 9:
            state[6] = 1
        if self.car[1] == 0:
            state[7] = 1
            
        return state
    
    
    def get_distance(self, state):
        distance = 0
        if self.battery != 0:
            x_gap = abs(self.customer[0] - self.car[0])
            y_gap = abs(self.customer[1] - self.car[1])
        else:
            x_gap = abs(self.depot[0] - self.car[0])
            y_gap = abs(self.depot[1] - self.car[1])
        distance = x_gap + y_gap
        
        return distance
      
        
    def go_up(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0] - 1,self.car[1]]
    
    def go_right(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]+1]
        
    def go_left(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]-1]
        
    def go_down(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0]+1,self.car[1]]  

        
    def reset_customer(self):
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        self.cus_needs_battery = 20
        
        if self.customer == self.car:
            self.reset_customer()
        
        self.grid[self.customer[0]][self.customer[1]] = 2
        
    

    def step(self, action):
        self.timesteps += 1
        self.reward = 0
        
        pre_state = self.get_state()
        pre_distance = self.get_distance(pre_state)
        
        if action == 0:
            self.go_up()
            if self.car[0] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 1:
            self.go_right()
            if self.car[1] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 2:
            self.go_down()
            if self.car[0] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 3:
            self.go_left()
            if self.car[1] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        
        self.grid[5][5] = 3
        self.grid[self.customer[0]][self.customer[1]] = 2
        self.grid[self.car[0]][self.car[1]] = 1
        state = self.get_state()
        distance = self.get_distance(state)
        
        if self.battery != 0:
            if self.car == self.customer:
                self.timesteps += 1
                self.reward += 10
                self.serviced_cars += 1
                self.battery -= 20
                
                self.reset_customer()
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        else:
            if self.car == self.depot:
                self.timesteps += 1
                self.reward += 10
                self.battery = 100
            
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        

        
        state = self.get_state()
                    
        return state, self.reward, self.done, self.info
                
                
                       

            
            
        
class MCS_random_battery(gym.Env):
    
    def __init__(self):
        
        self.grid = np.zeros([10,10])
        self.action_space = 4
        self.state_space = 9
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = np.random.randint(5,21)
        if self.battery != 0:
            self.cus_needs_battery = min(self.cus_needs_battery, self.battery)
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        
    
    def reset(self):
        self.state = np.zeros([8])
        self.grid = np.zeros([10,10])
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = np.random.randint(5,21)
        
        if self.battery != 0:
            self.cus_needs_battery = min(self.cus_needs_battery, self.battery)
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        state = self.get_state()
        return state
    
    
    def get_state(self):
        state = np.zeros(8)
        
        if self.battery == 0:
#             state[8] = 1
            if self.car[0] > self.depot[0]:
                state[0] = 1
            if self.car[1] < self.depot[1]:
                state[1] = 1
            if self.car[0] < self.depot[0]:
                state[2] = 1
            if self.car[1] > self.depot[1]:
                state[3] = 1
        
        else:
            if self.car[0] > self.customer[0]:
                state[0] = 1
            if self.car[1] < self.customer[1]:
                state[1] = 1
            if self.car[0] < self.customer[0]:
                state[2] = 1
            if self.car[1] > self.customer[1]:
                state[3] = 1
            
        if self.car[0] == 0:
            state[4] = 1
        if self.car[1] == 9:
            state[5] = 1
        if self.car[0] == 9:
            state[6] = 1
        if self.car[1] == 0:
            state[7] = 1
            
        return state
    
    
    def get_distance(self, state):
        distance = 0
        if self.battery != 0:
            x_gap = abs(self.customer[0] - self.car[0])
            y_gap = abs(self.customer[1] - self.car[1])
        else:
            x_gap = abs(self.depot[0] - self.car[0])
            y_gap = abs(self.depot[1] - self.car[1])
        distance = x_gap + y_gap
        
        return distance
      
        
    def go_up(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0] - 1,self.car[1]]
    
    def go_right(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]+1]
        
    def go_left(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]-1]
        
    def go_down(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0]+1,self.car[1]]  

        
    def reset_customer(self):
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        self.cus_needs_battery = np.random.randint(10,21)
        if self.battery != 0:
            self.cus_needs_battery = min(self.cus_needs_battery, self.battery)
        
        if self.customer == self.car:
            self.reset_customer()
        
        self.grid[self.customer[0]][self.customer[1]] = 2
        
    

    def step(self, action):
        self.timesteps += 1
        self.reward = 0
        
        pre_state = self.get_state()
        pre_distance = self.get_distance(pre_state)
        
        if action == 0:
            self.go_up()
            if self.car[0] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 1:
            self.go_right()
            if self.car[1] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 2:
            self.go_down()
            if self.car[0] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 3:
            self.go_left()
            if self.car[1] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        
        self.grid[5][5] = 3
        self.grid[self.customer[0]][self.customer[1]] = 2
        self.grid[self.car[0]][self.car[1]] = 1
        state = self.get_state()
        distance = self.get_distance(state)
        
        if self.battery != 0:
            if self.car == self.customer:
                self.timesteps += 1
                self.reward += 10
                self.serviced_cars += 1
                self.battery -= self.cus_needs_battery
                
                self.reset_customer()
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        else:
            if self.car == self.depot:
                self.timesteps += 1
                self.reward += 10
                self.battery = 100
            
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        
        
        state = self.get_state()
                    
        return state, self.reward, self.done, self.info        
    
    
    

    
    
class MCS_grid_state(gym.Env):
    
    def __init__(self):
        
        self.grid = np.zeros([10,10])
        self.action_space = 4
        self.state_space = 9
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        
    
    def reset(self):
        self.state = np.zeros([9])
        self.grid = np.zeros([10,10])
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        state = self.get_state()
        return state
    
    
    def get_state(self):
        state = self.grid.copy()
        
        if self.battery == 0:
            state[self.customer[0]][self.customer[1]] = 0
            state[self.depot[0]][self.depot[1]] = 2
        
        else:
            state[self.customer[0]][self.customer[1]] = 2
            state[self.depot[0]][self.depot[1]] = 0
            
        return state
    
    
    def get_distance(self):
        distance = 0
        if self.battery != 0:
            x_gap = abs(self.customer[0] - self.car[0])
            y_gap = abs(self.customer[1] - self.car[1])
        else:
            x_gap = abs(self.depot[0] - self.car[0])
            y_gap = abs(self.depot[1] - self.car[1])
        distance = x_gap + y_gap
        
        return distance
      
        
    def go_up(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0] - 1,self.car[1]]
    
    def go_right(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]+1]
        
    def go_left(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]-1]
        
    def go_down(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0]+1,self.car[1]]  

        
    def reset_customer(self):
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        self.cus_needs_battery = 20
        
        if self.customer == self.car:
            self.reset_customer()
        
        self.grid[self.customer[0]][self.customer[1]] = 2
        
    

    def step(self, action):
        self.timesteps += 1
        self.reward = 0
        
        pre_state = self.get_state()
        pre_distance = self.get_distance()
        
        if action == 0:
            self.go_up()
            if self.car[0] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 1:
            self.go_right()
            if self.car[1] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 2:
            self.go_down()
            if self.car[0] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 3:
            self.go_left()
            if self.car[1] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        
        self.grid[5][5] = 3
        self.grid[self.customer[0]][self.customer[1]] = 2
        self.grid[self.car[0]][self.car[1]] = 1
        state = self.get_state()
        distance = self.get_distance()
        
        if self.battery != 0:
            if self.car == self.customer:
                self.timesteps += 1
                self.reward += 10
                self.serviced_cars += 1
                self.battery -= 20
                
                self.reset_customer()
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        else:
            if self.car == self.depot:
                self.timesteps += 1
                self.reward += 10
                self.battery = 100
            
            else:
                if pre_distance - distance > 0:
                    self.reward += 1
                elif pre_distance - distance < 0:
                    self.reward -= 1
        

        
        state = self.get_state()
                    
        return state, self.reward, self.done, self.info
    
    
    
    
    
class MCS_less_reward(gym.Env):
    
    def __init__(self):
        
        self.grid = np.zeros([10,10])
        self.action_space = 4
        self.state_space = 9
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        
    
    def reset(self):
        self.state = np.zeros([8])
        self.grid = np.zeros([10,10])
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        state = self.get_state()
        return state
    
    
    def get_state(self):
        state = np.zeros(8)
        
        if self.battery == 0:
            if self.car[0] > self.depot[0]:
                state[0] = 1
            if self.car[1] < self.depot[1]:
                state[1] = 1
            if self.car[0] < self.depot[0]:
                state[2] = 1
            if self.car[1] > self.depot[1]:
                state[3] = 1
        
        else:
            if self.car[0] > self.customer[0]:
                state[0] = 1
            if self.car[1] < self.customer[1]:
                state[1] = 1
            if self.car[0] < self.customer[0]:
                state[2] = 1
            if self.car[1] > self.customer[1]:
                state[3] = 1
            
        if self.car[0] == 0:
            state[4] = 1
        if self.car[1] == 9:
            state[5] = 1
        if self.car[0] == 9:
            state[6] = 1
        if self.car[1] == 0:
            state[7] = 1
            
        return state
    
    
    def get_distance(self, state):
        distance = 0
        if self.battery != 0:
            x_gap = abs(self.customer[0] - self.car[0])
            y_gap = abs(self.customer[1] - self.car[1])
        else:
            x_gap = abs(self.depot[0] - self.car[0])
            y_gap = abs(self.depot[1] - self.car[1])
        distance = x_gap + y_gap
        
        return distance
      
        
    def go_up(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0] - 1,self.car[1]]
    
    def go_right(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]+1]
        
    def go_left(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]-1]
        
    def go_down(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0]+1,self.car[1]]  

        
    def reset_customer(self):
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        self.cus_needs_battery = 20
        
        if self.customer == self.car:
            self.reset_customer()
        
        self.grid[self.customer[0]][self.customer[1]] = 2
        
    

    def step(self, action):
        self.timesteps += 1
        self.reward = 0
        
        pre_state = self.get_state()
        pre_distance = self.get_distance(pre_state)
        
        if action == 0:
            self.go_up()
            if self.car[0] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 1:
            self.go_right()
            if self.car[1] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 2:
            self.go_down()
            if self.car[0] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 3:
            self.go_left()
            if self.car[1] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        
        self.grid[5][5] = 3
        self.grid[self.customer[0]][self.customer[1]] = 2
        self.grid[self.car[0]][self.car[1]] = 1
        state = self.get_state()
        distance = self.get_distance(state)
        
        if self.battery != 0:
            if self.car == self.customer:
                self.timesteps += 1
                self.reward += 10
                self.serviced_cars += 1
                self.battery -= 20
                
                self.reset_customer()

        else:
            if self.car == self.depot:
                self.timesteps += 1
                self.reward += 10
                self.battery = 100

        

        
        state = self.get_state()
                    
        return state, self.reward, self.done, self.info
    
    
    
class MCS_grid_state_less_reward(gym.Env):
    
    def __init__(self):
        
        self.grid = np.zeros([10,10])
        self.action_space = 4
        self.state_space = 9
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        
    
    def reset(self):
        self.state = np.zeros([9])
        self.grid = np.zeros([10,10])
        
        self.depot = [5,5]
        self.car = [5,5]
        self.grid[self.depot[0]][self.depot[1]] = 1   # supply car = 1, depot = 3
        
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        if self.customer == self.depot:
            self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        
        self.grid[self.customer[0]][self.customer[1]] = 2  # demand car = 2
        
        self.battery = 100
        self.cus_needs_battery = 20
        
        self.reward = 0
        self.serviced_cars = 0
        self.num_discharged_cars = 0
        self.timesteps = 0
        self.done = False
        self.info = None
        
        state = self.get_state()
        return state
    
    
    def get_state(self):
        state = self.grid.copy()
        
        if self.battery == 0:
            state[self.customer[0]][self.customer[1]] = 0
            state[self.depot[0]][self.depot[1]] = 2
        
        else:
            state[self.customer[0]][self.customer[1]] = 2
            state[self.depot[0]][self.depot[1]] = 0
            
        return state
    
    
    def get_distance(self):
        distance = 0
        if self.battery != 0:
            x_gap = abs(self.customer[0] - self.car[0])
            y_gap = abs(self.customer[1] - self.car[1])
        else:
            x_gap = abs(self.depot[0] - self.car[0])
            y_gap = abs(self.depot[1] - self.car[1])
        distance = x_gap + y_gap
        
        return distance
      
        
    def go_up(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0] - 1,self.car[1]]
    
    def go_right(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]+1]
        
    def go_left(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0],self.car[1]-1]
        
    def go_down(self):
        self.grid[self.car[0]][self.car[1]] = 0
        self.car = [self.car[0]+1,self.car[1]]  

        
    def reset_customer(self):
        self.customer = [np.random.randint(0,10), np.random.randint(0,10)]
        self.cus_needs_battery = 20
        
        if self.customer == self.car:
            self.reset_customer()
        
        self.grid[self.customer[0]][self.customer[1]] = 2
        
    

    def step(self, action):
        self.timesteps += 1
        self.reward = 0
        
        pre_state = self.get_state()
        pre_distance = self.get_distance()
        
        if action == 0:
            self.go_up()
            if self.car[0] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 1:
            self.go_right()
            if self.car[1] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 2:
            self.go_down()
            if self.car[0] > 9:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        elif action == 3:
            self.go_left()
            if self.car[1] < 0:
                self.reward -= 100
                self.done = True
                state = self.get_state()
                return state, self.reward, self.done, self.info
        
        self.grid[5][5] = 3
        self.grid[self.customer[0]][self.customer[1]] = 2
        self.grid[self.car[0]][self.car[1]] = 1
        state = self.get_state()
        distance = self.get_distance()
        
        if self.battery != 0:
            if self.car == self.customer:
                self.timesteps += 1
                self.reward += 10
                self.serviced_cars += 1
                self.battery -= 20
                
                self.reset_customer()
#             else:
#                 if pre_distance - distance > 0:
#                     self.reward += 1
#                 elif pre_distance - distance < 0:
#                     self.reward -= 1
        else:
            if self.car == self.depot:
                self.timesteps += 1
                self.reward += 10
                self.battery = 100
            
#             else:
#                 if pre_distance - distance > 0:
#                     self.reward += 1
#                 elif pre_distance - distance < 0:
#                     self.reward -= 1
        

        
        state = self.get_state()
                    
        return state, self.reward, self.done, self.info