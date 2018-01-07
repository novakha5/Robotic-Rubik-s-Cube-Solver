/**
  ******************************************************************************
  * @file    Project/STM32F4xx_StdPeriph_Templates/main.c 
  * @author  MCD Application Team
  * @version V1.8.0
  * @date    04-November-2016
  * @brief   Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; COPYRIGHT 2016 STMicroelectronics</center></h2>
  *
  * Licensed under MCD-ST Liberty SW License Agreement V2, (the "License");
  * You may not use this file except in compliance with the License.
  * You may obtain a copy of the License at:
  *
  *        http://www.st.com/software_license_agreement_liberty_v2
  *
  * Unless required by applicable law or agreed to in writing, software 
  * distributed under the License is distributed on an "AS IS" BASIS, 
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/** @addtogroup Template_Project
  * @{
  */ 

static __IO uint32_t uwTimingDelay;
RCC_ClocksTypeDef RCC_Clocks;

/* Private function prototypes -----------------------------------------------*/
static void Delay(__IO uint32_t nTime);
static void InitializeTimersEtc(void);
static void InitializeUsart(void);
static void UsartSend(const char *src);
/* Private functions ---------------------------------------------------------*/



#define MIN_TIMER_PERIOD    5000
#define MAX_TIMER_PERIOD    25000
#define PULSE_WIDTH         (MIN_TIMER_PERIOD / 2)
#define STEP_NUM						50
#define DIST_STEP_NUM				65

int TotalSteps[3] = {0, 0, 0}; //for every timer

int RemainingSteps[3] = {0, 0, 0};


#define RX_QUEUE_SIZE       8192
#define RX_QUEUE_SIZE_MASK  0x1FFF
char RxQueue[RX_QUEUE_SIZE] = {0, };

int RxQueueReadIndex = 0;
int RxQueueWriteIndex = 0;

int button = 0;
int done = 0;

//inicialize  Timer1, Timer2, Timer3, their counters and GPIO for Direction of the motor
//PWM compare and interrupts
void InitializeTimersEtc(void) 
{
  GPIO_InitTypeDef        GPIO_InitStructure;
  TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStruct;
  TIM_OCInitTypeDef       TIM_OCInitStruct;
  NVIC_InitTypeDef        NVIC_InitStructure;
 
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOE | RCC_AHB1Periph_GPIOA | RCC_AHB1Periph_GPIOC, ENABLE);
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2 | RCC_APB1Periph_TIM3, ENABLE);
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1, ENABLE);
  	
  /* GPIO STEP init for Timers */
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;  
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9 | GPIO_Pin_11;         // TIM1 AF mode
  GPIO_Init(GPIOE, &GPIO_InitStructure); 
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1 | GPIO_Pin_3;          // TIM2 AF mode
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_8;          // TIM3 AF mode
  GPIO_Init(GPIOC, &GPIO_InitStructure);
 
  GPIO_PinAFConfig(GPIOE, GPIO_PinSource9, GPIO_AF_TIM1);         // TIM1 AF config
  GPIO_PinAFConfig(GPIOE, GPIO_PinSource11, GPIO_AF_TIM1);
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource1, GPIO_AF_TIM2);         // TIM2 AF config
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource3, GPIO_AF_TIM2);
  GPIO_PinAFConfig(GPIOC, GPIO_PinSource6, GPIO_AF_TIM3);         // TIM3 AF config
  GPIO_PinAFConfig(GPIOC, GPIO_PinSource8, GPIO_AF_TIM3);

  /* GPIO DIR init */
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;  
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13 | GPIO_Pin_14;        // DIR (for tim1)
  GPIO_Init(GPIOE, &GPIO_InitStructure); 
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;                       // DIR (for tim2)
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
  GPIO_Init(GPIOC, &GPIO_InitStructure);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;                       // DIR (for tim3)
  GPIO_Init(GPIOC, &GPIO_InitStructure);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8;
  GPIO_Init(GPIOA, &GPIO_InitStructure);
 
	
	 /* Time base configuration */
  TIM_DeInit(TIM1);
  TIM_DeInit(TIM2);
  TIM_DeInit(TIM3);
  
  TIM_TimeBaseInitStruct.TIM_Prescaler = 31;
  TIM_TimeBaseInitStruct.TIM_CounterMode = TIM_CounterMode_Up;
  TIM_TimeBaseInitStruct.TIM_Period = MAX_TIMER_PERIOD;
  TIM_TimeBaseInitStruct.TIM_ClockDivision = TIM_CKD_DIV1;
  TIM_TimeBaseInitStruct.TIM_RepetitionCounter = 0;
  TIM_TimeBaseInit(TIM1, &TIM_TimeBaseInitStruct);
  TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStruct);
  TIM_TimeBaseInit(TIM3, &TIM_TimeBaseInitStruct);
  
  /* Set initial counter values */
  TIM_SetCounter(TIM1, PULSE_WIDTH + 1); // starts after impuls, so DRV has less problem to catch first impuls
  TIM_SetCounter(TIM2, PULSE_WIDTH + 1);
  TIM_SetCounter(TIM3, PULSE_WIDTH + 1);
  
  /* Output Compare (PWM) configuration */
  TIM_OCStructInit(&TIM_OCInitStruct);
  TIM_OCInitStruct.TIM_OCMode = TIM_OCMode_PWM1;
  TIM_OCInitStruct.TIM_OutputState = TIM_OutputState_Enable;
  TIM_OCInitStruct.TIM_Pulse = 0;
  
  TIM_OC1Init(TIM1, &TIM_OCInitStruct);
  TIM_OC2Init(TIM1, &TIM_OCInitStruct);
  TIM_OC2Init(TIM2, &TIM_OCInitStruct);
  TIM_OC4Init(TIM2, &TIM_OCInitStruct);
  TIM_OC1Init(TIM3, &TIM_OCInitStruct);
  TIM_OC3Init(TIM3, &TIM_OCInitStruct);  

  /* Interrupts */
  TIM_ITConfig(TIM1, TIM_IT_CC1, DISABLE);
  TIM_ITConfig(TIM1, TIM_IT_CC2, DISABLE);
  TIM_ITConfig(TIM2, TIM_IT_CC2, DISABLE);
  TIM_ITConfig(TIM2, TIM_IT_CC4, DISABLE);
  TIM_ITConfig(TIM3, TIM_IT_CC1, DISABLE);
  TIM_ITConfig(TIM3, TIM_IT_CC3, DISABLE);
  
  NVIC_InitStructure.NVIC_IRQChannel = TIM1_CC_IRQn; //interrupt request
  NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 8;
  NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
  NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
  NVIC_Init(&NVIC_InitStructure);

  NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
  NVIC_Init(&NVIC_InitStructure);

  NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;
  NVIC_Init(&NVIC_InitStructure);

  /* Power ON */
  TIM_CtrlPWMOutputs(TIM1, ENABLE);
  TIM_CCxCmd(TIM1, TIM_Channel_1, TIM_CCx_Enable);
  TIM_CCxCmd(TIM1, TIM_Channel_2, TIM_CCx_Enable);
  TIM_CCxCmd(TIM2, TIM_Channel_2, TIM_CCx_Enable);
  TIM_CCxCmd(TIM2, TIM_Channel_4, TIM_CCx_Enable);
  TIM_CCxCmd(TIM3, TIM_Channel_1, TIM_CCx_Enable);
  TIM_CCxCmd(TIM3, TIM_Channel_3, TIM_CCx_Enable);
  
 /* TIM_Cmd(TIM1, ENABLE);
  TIM_Cmd(TIM2, ENABLE);
  TIM_Cmd(TIM3, ENABLE);*/
}

//inicialize GPIO pins for USART2 (RX - pin_6, TX - pin_5), USART2 itself and it's interrupts
void InitializeUsart(void)
{
  GPIO_InitTypeDef        GPIO_InitStructure;
  USART_InitTypeDef       USART_InitStruct;
  NVIC_InitTypeDef        NVIC_InitStructure;
  
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
  	
  /* GPIO init for USART */
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_2MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;
  GPIO_InitStructure.GPIO_OType = GPIO_OType_OD; // Use "OpenDrain" because the pin is shared with USB overcurrent pin
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;   // Help the OD pin with Pull-up
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_6;          // USART2_TX, RX
  GPIO_Init(GPIOD, &GPIO_InitStructure); 
 
  GPIO_PinAFConfig(GPIOD, GPIO_PinSource5, GPIO_AF_USART2);
  GPIO_PinAFConfig(GPIOD, GPIO_PinSource6, GPIO_AF_USART2);

  /* USART init */
  USART_StructInit(&USART_InitStruct);
  USART_Init(USART2, &USART_InitStruct);
  USART_Cmd(USART2, ENABLE);
  
  /* Interrupt */
  NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
  NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 9;
  NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
  NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
  NVIC_Init(&NVIC_InitStructure);

  USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
}

//send string to Raspberry Pi when gets enable
void UsartSend(const char *src)
{
  while (*src != '\0') {
    while (USART_GetFlagStatus(USART2, USART_FLAG_TXE) != SET) {
      // wait
    }
    USART_SendData(USART2, *src);
    ++src;
  }
}

void UsartSendChar(char data)
{
  while (USART_GetFlagStatus(USART2, USART_FLAG_TXE) != SET) {
    // wait
  }
  USART_SendData(USART2, data);
}

void UsartSendInt(int data)
{
	char buffer[16] = {0, };
	char *ptr = buffer+15;
	if (data < 0) {
		UsartSend("-");
		data = -data;
	}
  while (data > 0) {
		*ptr = (data % 10) + '0';
		data = data / 10;
		--ptr;
	}
	if (ptr == buffer+15) {
		*ptr = '0';
		--ptr;
	}
	//UsartSend(ptr + 1);
}

//counts absolute value
int abs(int value){
	if (value < 0){
		value = -value;
	}
	return value;
}
//sets speed of the motor based on the distance from begining to end (speed up and down)
int SpeedCurve(int remainingSteps, int totalSteps)
{
  int x;
  int count;
  int absValue = abs((totalSteps/2) - remainingSteps);
  if(totalSteps == 50){
    x = totalSteps/5;
  } else if (totalSteps < 100){
    x = totalSteps/7;
  } else {
    x = totalSteps/10;
  }
  if((remainingSteps > x) && (remainingSteps < (totalSteps - x))){
    count = MIN_TIMER_PERIOD;
  } else 
	 count = (absValue * absValue * (20000/x)) + MIN_TIMER_PERIOD;
	if (count > MAX_TIMER_PERIOD){
		count = MAX_TIMER_PERIOD;
	}
	if (count < MIN_TIMER_PERIOD){
		count = MIN_TIMER_PERIOD;
	}
	return count;
}

//intecrrupt handler for TIM1 counting if the motor gets enough pulses and when send last it will disable timer1
void TIM1_CC_IRQHandler(void)
{
  RemainingSteps[0] -= 1;
  if (RemainingSteps[0] == 0) {
    TIM_Cmd(TIM1, DISABLE);
		TIM_SetCompare1(TIM1, 0);
		TIM_SetCompare2(TIM1, 0);
		TotalSteps[0] = 0;
    TIM_ITConfig(TIM1, TIM_IT_CC1, DISABLE);
    TIM_ITConfig(TIM1, TIM_IT_CC2, DISABLE);
  }
  TIM_SetAutoreload(TIM1, SpeedCurve(RemainingSteps[0], TotalSteps[0]));
  TIM_ClearITPendingBit(TIM1, TIM_IT_CC1);
  TIM_ClearITPendingBit(TIM1, TIM_IT_CC2);
}
 
//check if TIM2 have send enough pulses, if it sended last one, will disable timer2
void TIM2_IRQHandler(void)
{
  RemainingSteps[1] -= 1;
  if (RemainingSteps[1] == 0) {
    TIM_Cmd(TIM2, DISABLE);
		TIM_SetCompare2(TIM2, 0);
		TIM_SetCompare4(TIM2, 0);
		TotalSteps[1] = 0;
    TIM_ITConfig(TIM2, TIM_IT_CC2, DISABLE);
    TIM_ITConfig(TIM2, TIM_IT_CC4, DISABLE);
  }
  TIM_SetAutoreload(TIM2, SpeedCurve(RemainingSteps[1], TotalSteps[1]));
  TIM_ClearITPendingBit(TIM2, TIM_IT_CC2);
  TIM_ClearITPendingBit(TIM2, TIM_IT_CC4);
}

//check if TIM3 have send enough pulses, if it sended last one, will disable timer3
void TIM3_IRQHandler(void)
{
  RemainingSteps[2] -= 1;
  if (RemainingSteps[2] == 0) {
    TIM_Cmd(TIM3, DISABLE);
		TIM_SetCompare1(TIM3, 0);
		TIM_SetCompare3(TIM3, 0);
		TotalSteps[2] = 0;
    TIM_ITConfig(TIM3, TIM_IT_CC1, DISABLE);
    TIM_ITConfig(TIM3, TIM_IT_CC3, DISABLE);    
  }
  TIM_SetAutoreload(TIM3, SpeedCurve(RemainingSteps[2], TotalSteps[2]));
  TIM_ClearITPendingBit(TIM3, TIM_IT_CC1);
  TIM_ClearITPendingBit(TIM3, TIM_IT_CC3);
}

int isBufferEmpty(void){
	__disable_irq();
	int ret = 0;
	if (RxQueueReadIndex == RxQueueWriteIndex){
		ret = 1;
	}
	__enable_irq();
	return ret;
}

int isBufferFull(void){
	int ret = 0;
	if (((RxQueueWriteIndex + 1) & RX_QUEUE_SIZE_MASK) == RxQueueReadIndex){
		ret = 1;
	}
	return ret;
}

char readBuffer(){
	if(isBufferEmpty()){
		return 1;
	}
	__disable_irq();
	char read = RxQueue[RxQueueReadIndex];
	RxQueueReadIndex = (RxQueueReadIndex + 1) & RX_QUEUE_SIZE_MASK;
	__enable_irq();
	return read;
}

int writeToBuffer(char data){
	if (isBufferFull()){
		while(1){}
	}
	RxQueue[RxQueueWriteIndex] = data;
  RxQueueWriteIndex = (RxQueueWriteIndex + 1) & RX_QUEUE_SIZE_MASK;
	return 0;
}

void USART2_IRQHandler(void){
	int data =  USART_ReceiveData(USART2);
	writeToBuffer(data);
	USART_ClearITPendingBit(USART2, USART_IT_RXNE);
}

void clearBuffer(void){
	__disable_irq();
	RxQueueWriteIndex = 0;
	RxQueueReadIndex = 0;
	__enable_irq();
}

int main(void)
{
  button = 0;
  GPIO_InitTypeDef GPIO_InitStructure;
  RCC_GetClocksFreq(&RCC_Clocks);
  SysTick_Config(RCC_Clocks.HCLK_Frequency / 100);
  Delay(5);
  
  /* LED */
	
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD | RCC_AHB1Periph_GPIOE, ENABLE);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12; //green
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;  
  GPIO_Init(GPIOD, &GPIO_InitStructure);
  
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_15; //blue
  GPIO_Init(GPIOD, &GPIO_InitStructure);
	
	/*DRV sleep, reset*/
	GPIO_ResetBits(GPIOE, GPIO_Pin_12);
	GPIO_Init(GPIOE, &GPIO_InitStructure);
	
  /* User button */
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN;
  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;  
  GPIO_Init(GPIOA, &GPIO_InitStructure);
      
  InitializeTimersEtc();
  InitializeUsart();

  UsartSend("\r\nReady\r\n");
  
  while(1){
    if(isBufferEmpty()){
    
    }
    else {
      int data = readBuffer();
      if(data == 'R'){
        break;
      }
    }
  }
  
  GPIO_SetBits(GPIOE, GPIO_Pin_15);
  
	while(button != 10000){
		if(GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == Bit_SET){
			button++;
		} else {
			button--;
			if(button < 0){
				button = 0;
			}
		}
	}
  button = 0;
	clearBuffer();
	UsartSend("\r\nStart\r\n");
  GPIO_SetBits(GPIOE, GPIO_Pin_12);
  GPIO_ResetBits(GPIOE, GPIO_Pin_15);
	
  /* Infinite loop */
  while (1){
    if (USART_GetFlagStatus(USART2, USART_FLAG_NE) == SET) {
      UsartSend("\r\nNOISE DETECTED!\r\n");
    }
    if (USART_GetFlagStatus(USART2, USART_FLAG_ORE) == SET) {
      UsartSend("\r\nOVERRUN DETECTED!\r\n");
    }
    if (USART_GetFlagStatus(USART2, USART_FLAG_FE) == SET) {
      UsartSend("\r\nFRAMING ERROR DETECTED!\r\n");
    }
    if (!isBufferEmpty()) {
      int data = readBuffer();
			GPIO_SetBits(GPIOD, GPIO_Pin_12);
      switch (data) {
        case ' ':
				case '\r':
          // Reset timer counter values
          TIM_SetCounter(TIM1, PULSE_WIDTH + 1);
          TIM_SetCounter(TIM2, PULSE_WIDTH + 1);
          TIM_SetCounter(TIM3, PULSE_WIDTH + 1);
          // Enable one timer (only)
          if (TotalSteps[0] > 0) {
            RemainingSteps[0] = TotalSteps[0];
            TIM_Cmd(TIM1, ENABLE);
          } else if (TotalSteps[1] > 0) {
            RemainingSteps[1] = TotalSteps[1];
            TIM_Cmd(TIM2, ENABLE);
          } else if (TotalSteps[2] > 0) {
            RemainingSteps[2] = TotalSteps[2];
            TIM_Cmd(TIM3, ENABLE);
          }
					while(RemainingSteps[0] != 0 || RemainingSteps[1] != 0 || RemainingSteps[2] != 0){
				 		//wait
					}
          UsartSend("\r\nDone\r\n");
          Delay(10);
          break;
        case 'A':
          TIM_SetCompare1(TIM1, PULSE_WIDTH); // left motor will STEP
          GPIO_ResetBits(GPIOE, GPIO_Pin_13); // forward DIR
          TotalSteps[0] = STEP_NUM;						// 90° angle
          TIM_ITConfig(TIM1, TIM_IT_CC1, ENABLE);
					break;
        case 'a':
          TIM_SetCompare1(TIM1, PULSE_WIDTH); // left motor will STEP          
          GPIO_SetBits(GPIOE, GPIO_Pin_13);   // reverse DIR
          TotalSteps[0] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM1, TIM_IT_CC1, ENABLE);
					break;
				case 'B':
          TIM_SetCompare2(TIM1, PULSE_WIDTH); // right motor will STEP
          GPIO_ResetBits(GPIOE, GPIO_Pin_14); // forward DIR
          TotalSteps[0] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM1, TIM_IT_CC2, ENABLE);
					break;
				case 'b':
          TIM_SetCompare2(TIM1, PULSE_WIDTH); // right motor will STEP
          GPIO_SetBits(GPIOE, GPIO_Pin_14);   // reverse DIR
          TotalSteps[0] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM1, TIM_IT_CC2, ENABLE);
					break;
				case 'C':
          TIM_SetCompare2(TIM2, PULSE_WIDTH); // up motor will STEP
          GPIO_ResetBits(GPIOC, GPIO_Pin_2);  // forward DIR
          TotalSteps[1] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM2, TIM_IT_CC2, ENABLE);
					break;
				case 'c':
          TIM_SetCompare2(TIM2, PULSE_WIDTH); // up motor will STEP
          GPIO_SetBits(GPIOC, GPIO_Pin_2);    // reverse DIR
          TotalSteps[1] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM2, TIM_IT_CC2, ENABLE);
					break;
				case 'D':
          TIM_SetCompare4(TIM2, PULSE_WIDTH); // down motor will STEP
          GPIO_ResetBits(GPIOA, GPIO_Pin_2);  // forward DIR
          TotalSteps[1] = STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM2, TIM_IT_CC4, ENABLE);
					break;
				case 'd':
          TIM_SetCompare4(TIM2, PULSE_WIDTH); // down motor will STEP
          GPIO_SetBits(GPIOA, GPIO_Pin_2);    // reverse DIR
          TotalSteps[1] = STEP_NUM;           // 90° angle  
          TIM_ITConfig(TIM2, TIM_IT_CC4, ENABLE);
					break;
				case 'E':
          TIM_SetCompare1(TIM3, PULSE_WIDTH); // horizontal motor will STEP
          GPIO_ResetBits(GPIOC, GPIO_Pin_9);  // forward DIR
          TotalSteps[2] = DIST_STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM3, TIM_IT_CC1, ENABLE);
					break;
				case 'e':
          TIM_SetCompare1(TIM3, PULSE_WIDTH); // horizontal motor will STEP
          GPIO_SetBits(GPIOC, GPIO_Pin_9);    // reverse DIR
          TotalSteps[2] = DIST_STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM3, TIM_IT_CC1, ENABLE);
					break;
        case 'F':
          TIM_SetCompare3(TIM3, PULSE_WIDTH); // vertical motor will STEP
          GPIO_ResetBits(GPIOA, GPIO_Pin_8);  // forward DIR
          TotalSteps[2] = DIST_STEP_NUM;           // 90° angle
          TIM_ITConfig(TIM3, TIM_IT_CC3, ENABLE);
					break;
				case 'f':
          TIM_SetCompare3(TIM3, PULSE_WIDTH); // vertical motor will STEP
          GPIO_SetBits(GPIOA, GPIO_Pin_8);    // reverse DIR
          TotalSteps[2] = DIST_STEP_NUM;           // 90° angle  
          TIM_ITConfig(TIM3, TIM_IT_CC3, ENABLE);
          break;
				case '2':
					TotalSteps[0] = 2*TotalSteps[0];		//180° angle
					TotalSteps[1] = 2*TotalSteps[1];
					TotalSteps[2] = 2*TotalSteps[2];
					break;
        case 's':
          TotalSteps[0] = TotalSteps[0]/10;		//small steps
					TotalSteps[1] = TotalSteps[1]/10;
					TotalSteps[2] = TotalSteps[2]/10;
          break;
        case '.':
          done = 1;
          UsartSend("\r\nCompleate\r\n"); 
          break;
        default:
          UsartSend("\r\nIgnoring unknown command\r\n");
      }
    } else {
      if(done == 1){
        GPIO_ResetBits(GPIOE, GPIO_Pin_12);
        while(button != 10000){
          if(GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == Bit_SET){
            button++;
          } else {
            button--;
            if(button < 0){
              button = 0;
            }
          }
         }
        GPIO_SetBits(GPIOE, GPIO_Pin_12);
        clearBuffer();
        UsartSend("\r\nStart\r\n");
        done = 0; 
      }
    }
  }
}

/**
  * @brief  Inserts a delay time.
  * @param  nTime: specifies the delay time length, in milliseconds.
  * @retval None
  */
void Delay(__IO uint32_t nTime)
{ 
  uwTimingDelay = nTime;

  while(uwTimingDelay != 0);
}

/**
  * @brief  Decrements the TimingDelay variable.
  * @param  None
  * @retval None
  */
void TimingDelay_Decrement(void)
{
  if (uwTimingDelay != 0x00)
  { 
    uwTimingDelay--;
  }
}

#ifdef  USE_FULL_ASSERT

/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{ 
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */

  /* Infinite loop */
  while (1)
  {
  }
}
#endif

/**
  * @}
  */


/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
